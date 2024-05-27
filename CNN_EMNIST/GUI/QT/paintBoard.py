import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QPixmap, QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPoint, QSize


class PaintBoard(QWidget):
    def __init__(self,  Size=QSize(911, 261), Fill=QColor(255, 255, 255, 255)):
        super().__init__()

        self.__size = Size
        self.__fill = Fill
        self.__thickness = 18
        self.__penColor = QColor(0, 0, 0, 255)
        self.__begin_point = QPoint()
        self.__end_point = QPoint()

        self.__board = QPixmap(self.__size)
        self.__board.fill(Fill)
        self.setFixedSize(self.__size)
        self.__painter = QPainter()

    def Clear(self):
        self.__board.fill(self.__fill)
        self.update()

    def setBoardFill(self, fill):
        self.__fill = fill
        self.__board.fill(fill)
        self.update()

    def setPenColor(self, color):
        self.__penColor = color

    def setPenThickness(self, thickness=20):
        self.__thickness = thickness

    def getContentAsQImage(self):
        image = self.__board.toImage()
        return image

    def paintEvent(self, paintEvent):
        self.__painter.begin(self)
        self.__painter.drawPixmap(0, 0, self.__board)
        self.__painter.end()

    def mousePressEvent(self, mouseEvent):
        if mouseEvent.button() == Qt.LeftButton:
            self.__begin_point = mouseEvent.pos()
            self.__end_point = self.__begin_point

    def mouseMoveEvent(self, mouseEvent):
        if mouseEvent.buttons() == Qt.LeftButton:
            self.__end_point = mouseEvent.pos()

            self.__painter.begin(self.__board)
            self.__painter.setPen(QPen(self.__penColor, self.__thickness))
            self.__painter.drawLine(self.__begin_point, self.__end_point)
            self.__painter.end()
            self.__begin_point = self.__end_point
            self.update()

