import sys
import os
from PIL import Image, ImageQt
from CNN.opencv import Images_Processing
from QT.layout import Ui_MainWindow
from QT.paintBoard import PaintBoard
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QMessageBox, QFileDialog, QApplication
from PyQt5.QtGui import QColor, QPixmap
import tensorflow as tf
import cv2
from CNN.opencv import *
from CNN.train import CNN

FILE_MODE = 1  # 打开文件
WRITE_MODE = 2  # 手写输入

def Words_Predict(image_path):
    try:
        latest = tf.train.latest_checkpoint('./CNN/ckpt')
        cnn = CNN()
        status = cnn.model.load_weights(latest)
        status.expect_partial()  
        
        print(f"Opening image: {image_path}")  # Debug: print the image path
        img = Image.open(image_path).convert('L').transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_90)
        flatten_img = np.reshape(img, (1, 28, 28, 1))
        x = np.array(flatten_img)
        y = cnn.model.predict(x)
        temp = np.argmax(y) + 96
        return temp
    except Exception as e:
        print(f"Error in Words_Predict: {e}")
        return None

class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.mode = FILE_MODE
        self.result = []
        self.setupUi(self)
        self.center()

        self.paintBoard = PaintBoard()
        self.paintBoard.setPenColor(QColor(0, 0, 0, 0))
        self.dArea_Layout.addWidget(self.paintBoard)
        self.clearDataArea()

    def center(self):
        framePos = self.frameGeometry()
        scPos = QDesktopWidget().availableGeometry().center()
        framePos.moveCenter(scPos)
        self.move(framePos.topLeft())

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.Yes)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def clearDataArea(self):
        self.paintBoard.Clear()
        self.lbDataArea.clear()
        self.teResult.clear()
        self.result = [0]

    def cbBox_Mode_Callback(self, text):
        if text == '1：打开图像文件':
            self.mode = FILE_MODE
            self.clearDataArea()
            self.pbtOpenImage.setEnabled(True)
            self.lbDataArea.setVisible(True)
            self.paintBoard.setBoardFill(QColor(0, 0, 0, 0))
            self.paintBoard.setPenColor(QColor(0, 0, 0, 0))

        elif text == '2：鼠标手写输入':
            self.mode = WRITE_MODE
            self.clearDataArea()
            self.pbtOpenImage.setEnabled(False)
            self.lbDataArea.setVisible(False)
            self.paintBoard.setBoardFill(QColor(0, 0, 0, 255))
            self.paintBoard.setPenColor(QColor(255, 255, 255, 255))

    def pbtClear_Callback(self):
        self.clearDataArea()

    def pbtPredict_Callback(self):
        if self.mode == WRITE_MODE:
            base_dir = 'c:/origin/'
            dst_dir = 'c:/result/'
            img = self.paintBoard.getContentAsQImage()
            pil_img = ImageQt.fromqimage(img)
            pil_img.save('c:/origin/1.png')
            image = cv2.imread(base_dir + '1.png')
            count = Images_Processing(base_dir, dst_dir)
        else:
            base_dir = imageName
            dst_dir = 'c:/openresult/'
            count = Images_Processing(base_dir, dst_dir)
        for i in range(count):
            imgpath = (dst_dir + '%d.png' % (i+1))
            
            temp = Words_Predict(imgpath)
            self.teResult.insertPlainText(chr(temp))

    def pbtOpenImage_Callback(self):
        self.clearDataArea()
        global imageName
        imageName, _ = QFileDialog.getOpenFileName(self, '打开文件', '.', '(*.jpg *.png)')
        pix = QPixmap(imageName).scaled(self.lbDataArea.width(), self.lbDataArea.height())
        self.lbDataArea.setPixmap(pix)

if __name__ == "__main__":
    if not os.path.exists('c:/openresult/'):
        os.makedirs('c:/origin/')
        os.makedirs('c:/result/')
        os.makedirs('c:/openresult')
    app = QApplication(sys.argv)
    Gui = MainWindow()
    Gui.show()
    sys.exit(app.exec_())

