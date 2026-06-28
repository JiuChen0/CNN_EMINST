import os
import sys
import tempfile
from pathlib import Path

import numpy as np
import tensorflow as tf
from PIL import Image, ImageQt
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QDesktopWidget,
    QFileDialog,
    QMainWindow,
    QMessageBox,
)

from CNN.opencv import segment_characters
from CNN.train import CNN, DEFAULT_CHECKPOINT_DIR
from QT.layout import Ui_MainWindow
from QT.paintBoard import PaintBoard


FILE_MODE = 1  # 打开文件
WRITE_MODE = 2  # 手写输入
APP_DIR = Path(__file__).resolve().parent
BUNDLED_CHECKPOINT_DIR = APP_DIR / "CNN" / "ckpt"


class LetterPredictor:
    """Load the network once and recognize a batch of segmented letters."""

    def __init__(self):
        configured = os.environ.get("CNN_EMNIST_CHECKPOINT_DIR")
        search_dirs = [
            Path(configured).expanduser() if configured else DEFAULT_CHECKPOINT_DIR,
            BUNDLED_CHECKPOINT_DIR,
        ]
        latest = next(
            (
                checkpoint
                for directory in search_dirs
                if (checkpoint := tf.train.latest_checkpoint(str(directory)))
            ),
            None,
        )
        if latest is None:
            raise FileNotFoundError(
                "No model checkpoint was found. Train the model first with "
                "`python -m CNN.train`, or set CNN_EMNIST_CHECKPOINT_DIR."
            )

        self.model = CNN().model
        status = self.model.load_weights(latest)
        status.expect_partial()

    def predict(self, image_paths):
        transpose = getattr(Image, "Transpose", Image)
        images = []
        for image_path in image_paths:
            with Image.open(image_path) as image:
                image = (
                    image.convert("L")
                    .transpose(transpose.FLIP_LEFT_RIGHT)
                    .transpose(transpose.ROTATE_90)
                )
                images.append(np.asarray(image, dtype=np.float32) / 255.0)

        batch = np.stack(images)[..., np.newaxis]
        scores = self.model.predict(batch, verbose=0)
        class_indexes = np.argmax(scores, axis=1)
        if np.any((class_indexes < 1) | (class_indexes > 26)):
            invalid = class_indexes[(class_indexes < 1) | (class_indexes > 26)]
            raise RuntimeError(
                f"Model returned invalid class indexes: {invalid.tolist()}"
            )
        return "".join(chr(int(index) + 96) for index in class_indexes)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.mode = FILE_MODE
        self.result = []
        self.image_name = None
        self.predictor = None
        self.temporary_dir = tempfile.TemporaryDirectory(prefix="cnn-emnist-")
        self.work_dir = Path(self.temporary_dir.name)
        self.setupUi(self)
        self.center()

        self.paintBoard = PaintBoard()
        self.paintBoard.setPenColor(QColor(0, 0, 0, 0))
        self.dArea_Layout.addWidget(self.paintBoard)
        self.clearDataArea()

    def center(self):
        frame_position = self.frameGeometry()
        screen_position = QDesktopWidget().availableGeometry().center()
        frame_position.moveCenter(screen_position)
        self.move(frame_position.topLeft())

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Message",
            "Are you sure to quit?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes,
        )
        if reply == QMessageBox.Yes:
            self.temporary_dir.cleanup()
            event.accept()
        else:
            event.ignore()

    def clearDataArea(self):
        self.paintBoard.Clear()
        self.lbDataArea.clear()
        self.teResult.clear()
        self.result = []
        self.image_name = None

    def cbBox_Mode_Callback(self, text):
        if text == "1：打开图像文件":
            self.mode = FILE_MODE
            self.clearDataArea()
            self.pbtOpenImage.setEnabled(True)
            self.lbDataArea.setVisible(True)
            self.paintBoard.setBoardFill(QColor(0, 0, 0, 0))
            self.paintBoard.setPenColor(QColor(0, 0, 0, 0))

        elif text == "2：鼠标手写输入":
            self.mode = WRITE_MODE
            self.clearDataArea()
            self.pbtOpenImage.setEnabled(False)
            self.lbDataArea.setVisible(False)
            self.paintBoard.setBoardFill(QColor(0, 0, 0, 255))
            self.paintBoard.setPenColor(QColor(255, 255, 255, 255))

    def pbtClear_Callback(self):
        self.clearDataArea()

    def pbtPredict_Callback(self):
        try:
            if self.mode == WRITE_MODE:
                image_path = self.work_dir / "handwriting.png"
                image = self.paintBoard.getContentAsQImage()
                ImageQt.fromqimage(image).save(image_path)
            else:
                if not self.image_name:
                    QMessageBox.information(self, "提示", "请先选择一张图片。")
                    return
                image_path = self.image_name

            character_paths = segment_characters(
                image_path, self.work_dir / "characters"
            )
            if not character_paths:
                QMessageBox.information(self, "提示", "没有检测到可识别的字符。")
                return

            if self.predictor is None:
                self.predictor = LetterPredictor()
            self.teResult.setPlainText(self.predictor.predict(character_paths))
        except Exception as error:
            QMessageBox.critical(self, "识别失败", str(error))

    def pbtOpenImage_Callback(self):
        image_name, _ = QFileDialog.getOpenFileName(
            self, "打开文件", ".", "Images (*.jpg *.jpeg *.png)"
        )
        if not image_name:
            return

        self.clearDataArea()
        self.image_name = Path(image_name)
        pixmap = QPixmap(image_name).scaled(
            self.lbDataArea.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        )
        self.lbDataArea.setPixmap(pixmap)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec_())
