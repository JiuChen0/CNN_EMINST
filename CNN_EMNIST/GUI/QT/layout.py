# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'layout'

# Created by: PyQt5 UI code generator 5.9.2

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(958, 720)
        self.cbBox_Mode = QtWidgets.QComboBox(MainWindow)
        self.cbBox_Mode.setGeometry(QtCore.QRect(670, 130, 221, 30))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(10)
        self.cbBox_Mode.setFont(font)
        self.cbBox_Mode.setIconSize(QtCore.QSize(30, 30))
        self.cbBox_Mode.setObjectName("cbBox_Mode")
        self.cbBox_Mode.addItem("")
        self.cbBox_Mode.addItem("")
        self.label = QtWidgets.QLabel(MainWindow)
        self.label.setGeometry(QtCore.QRect(710, 80, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pbtClear = QtWidgets.QPushButton(MainWindow)
        self.pbtClear.setGeometry(QtCore.QRect(800, 620, 120, 41))
        self.pbtClear.setStyleSheet("")
        self.pbtClear.setCheckable(False)
        self.pbtClear.setChecked(False)
        self.pbtClear.setObjectName("pbtClear")
        self.pbtOpenImage = QtWidgets.QPushButton(MainWindow)
        self.pbtOpenImage.setGeometry(QtCore.QRect(500, 620, 121, 41))
        self.pbtOpenImage.setCheckable(False)
        self.pbtOpenImage.setObjectName("pbtOpenImage")
        self.pbtPredict = QtWidgets.QPushButton(MainWindow)
        self.pbtPredict.setGeometry(QtCore.QRect(650, 620, 120, 41))
        self.pbtPredict.setStyleSheet("")
        self.pbtPredict.setObjectName("pbtPredict")
        self.label_3 = QtWidgets.QLabel(MainWindow)
        self.label_3.setGeometry(QtCore.QRect(20, 600, 91, 71))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(MainWindow)
        self.label_4.setGeometry(QtCore.QRect(20, 230, 271, 41))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(MainWindow)
        self.label_5.setGeometry(QtCore.QRect(10, 10, 631, 191))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(8)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.verticalLayoutWidget = QtWidgets.QWidget(MainWindow)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 290, 911, 261))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.dArea_Layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.dArea_Layout.setContentsMargins(0, 0, 0, 0)
        self.dArea_Layout.setSpacing(0)
        self.dArea_Layout.setObjectName("dArea_Layout")
        self.lbDataArea = QtWidgets.QLabel(MainWindow)
        self.lbDataArea.setGeometry(QtCore.QRect(20, 290, 911, 261))
        self.lbDataArea.setMouseTracking(False)
        self.lbDataArea.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lbDataArea.setFrameShape(QtWidgets.QFrame.Box)
        self.lbDataArea.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.lbDataArea.setLineWidth(4)
        self.lbDataArea.setMidLineWidth(0)
        self.lbDataArea.setText("")
        self.lbDataArea.setObjectName("lbDataArea")
        self.teResult = QtWidgets.QTextEdit(MainWindow)
        self.teResult.setGeometry(QtCore.QRect(130, 580, 341, 111))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(36)
        self.teResult.setFont(font)
        self.teResult.setObjectName("teResult")
        self.label_7 = QtWidgets.QLabel(MainWindow)
        self.label_7.setGeometry(QtCore.QRect(540, 230, 391, 31))
        font = QtGui.QFont()
        font.setFamily("Agency FB")
        font.setPointSize(18)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")

        self.retranslateUi(MainWindow)
        self.cbBox_Mode.activated['QString'].connect(MainWindow.cbBox_Mode_Callback)
        self.pbtClear.clicked.connect(MainWindow.pbtClear_Callback)
        self.pbtPredict.clicked.connect(MainWindow.pbtPredict_Callback)
        self.pbtOpenImage.clicked.connect(MainWindow.pbtOpenImage_Callback)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "手写英文字母识别1.0 --by Baijindi"))
        MainWindow.setWhatsThis(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.cbBox_Mode.setItemText(0, _translate("MainWindow", "1：打开图像文件"))
        self.cbBox_Mode.setItemText(1, _translate("MainWindow", "2：鼠标手写输入"))
        self.label.setText(_translate("MainWindow", "请选择模式："))
        self.pbtClear.setText(_translate("MainWindow", "清除数据"))
        self.pbtOpenImage.setText(_translate("MainWindow", "打开图片"))
        self.pbtPredict.setText(_translate("MainWindow", "识别"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">识别结果：</span></p></body></html>"))
        self.label_4.setText(_translate("MainWindow", "请在下方进行手写输入"))
        self.label_5.setText(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:600;\">使用说明</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:11pt;\">1、点击下拉列表进行模式选择，输入待识别数据</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:11pt;\">2、点击“识别”按钮进行识别,经CNN网络计算后输出显示识别结果</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:11pt;\">3、点击“清除数据”按钮重新输入数据</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:11pt;\">模式1：使用已有图像文件作为待识别数据</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Ubuntu\'; font-size:11pt;\">模式2：使用鼠标在数据输入区域手写输入作为待识别数据</span></p></body></html>"))
        self.label_7.setText(_translate("MainWindow", "手写时请勿触碰手写框边界！"))

