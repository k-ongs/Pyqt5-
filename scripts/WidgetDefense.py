# -*- coding: utf-8 -*-
import cv2
import time
from scripts.QClickLabel import QClickLabel
from PyQt5.QtGui import QPixmap, QImage, QCursor
from scripts.scriptsss import sp_noise, gasuss_noise
from PyQt5.QtCore import pyqtSignal,QThread, QSize, Qt
from PyQt5.QtWidgets import QLabel, QWidget, QGridLayout, QSizePolicy, QHBoxLayout, QPushButton, QSpacerItem, QTextBrowser

# 采用线程来播放视频
class Thread(QThread):
    isRun = False
    algorithm = True
    __algorithm_im = False
    console = pyqtSignal(str)
    setSourceImage = pyqtSignal(object)
    setHandleImage = pyqtSignal(object)

    def run(self):
        capture = cv2.VideoCapture(0)
        if not capture.isOpened():
            self.console.emit("摄像头启动失败！")
            return
        self.isRun = True
        self.console.emit("摄像头已启动")

        face_detector = cv2.CascadeClassifier(r'./data/haarcascade_frontalface_default.xml')
        while self.isRun and capture.isOpened():
            if self.__algorithm_im != self.algorithm:
                if self.algorithm:
                    im = cv2.imread("./data/img/ylx.png")
                else:
                    im = cv2.imread("./data/img/pmj.jpg")
                self.__algorithm_im = self.algorithm

            ret, frame = capture.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + w), (255, 0, 0))
                if ret:
                    frame2 = frame.copy()
                    frame2[0:200, 0:150] = im
                    rgbImage_right = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
                    if self.algorithm:
                        rgbImage_right[x:x + w, y:y + w] = sp_noise(rgbImage_right[x:x + w, y:y + w], 0.0001)

                    rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
                    convertToQtFormat_right = QImage(rgbImage_right.data, rgbImage_right.shape[1],rgbImage_right.shape[0],QImage.Format_RGB888)
                    self.setSourceImage.emit(convertToQtFormat)
                    self.setHandleImage.emit(convertToQtFormat_right)
                else:
                    break
            time.sleep(0.02)
        self.isRun = False
        self.__algorithm_im = not self.algorithm
        self.setSourceImage.emit(None)
        self.setHandleImage.emit(None)
        self.console.emit("摄像头已关闭")

class widgetDefense(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        # 定义网格布局
        self.widgetDefenseGridLayout = QGridLayout(self)
        self.widgetDefenseGridLayout.setContentsMargins(15, 14, 15, 10)
        self.widgetDefenseGridLayout.setHorizontalSpacing(10)
        self.widgetDefenseGridLayout.setVerticalSpacing(0)
        self.widgetDefenseGridLayout.setObjectName("widgetDefenseGridLayout")

        # 添加一个Label显示处理前的图像
        self.labelSourceImage = QClickLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelSourceImage.sizePolicy().hasHeightForWidth())
        self.labelSourceImage.setSizePolicy(sizePolicy)
        self.labelSourceImage.setMinimumSize(QSize(200, 200))
        self.labelSourceImage.setCursor(QCursor(Qt.PointingHandCursor))
        self.labelSourceImage.clicked(self.__labelSourceImageClick)

        # 添加一个标签显示"视频源："
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.labelTitle1 = QLabel(self)
        self.labelTitle1.setMinimumSize(QSize(0, 30))
        self.labelTitle1.setMaximumSize(QSize(16777215, 30))
        self.labelTitle1.setStyleSheet("font: 75 13pt \'微软雅黑\';")
        self.labelTitle1.setObjectName("labelTitle1")
        self.labelTitle1.setText("视频源：")
        self.horizontalLayout_3.addWidget(self.labelTitle1)
        self.pushButton = QPushButton(self)
        self.pushButton.setEnabled(True)
        self.pushButton.setMinimumSize(QSize(80, 26))
        self.pushButton.setMaximumSize(QSize(80, 16777215))
        self.pushButton.setStyleSheet("QPushButton{background-color: rgb(222, 222, 222);border:1px solid rgb(191, 191, 191);}QPushButton:hover{background-color: rgba(200, 200, 200, 255);}QPushButton:pressed{background-color: rgb(222, 222, 222);}")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.pushButton.setText("噪声攻击")
        self.pushButton.clicked.connect(self.__pushButtonClick)
        self.horizontalLayout_3.addWidget(self.pushButton)
        self.widgetDefenseGridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)

        # 添加一个Label显示处理后的图像
        self.labelHandleImage = QClickLabel(self)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelHandleImage.sizePolicy().hasHeightForWidth())
        self.labelHandleImage.setSizePolicy(sizePolicy)
        self.labelHandleImage.setMinimumSize(QSize(200, 200))
        self.labelHandleImage.setCursor(QCursor(Qt.PointingHandCursor))
        self.labelHandleImage.clicked(self.__labelSourceImageClick)
        self.widgetDefenseGridLayout.addWidget(self.labelHandleImage, 5, 1, 1, 1)

        # 添加一个标签显示"处理后："
        self.widgetDefenseGridLayout.addWidget(self.labelSourceImage, 5, 0, 1, 1)
        self.labelTitle2 = QLabel(self)
        self.labelTitle2.setMaximumSize(QSize(16777215, 30))
        self.labelTitle2.setStyleSheet("font: 75 13pt \'微软雅黑\';")
        self.labelTitle2.setObjectName("labelTitle2")
        self.widgetDefenseGridLayout.addWidget(self.labelTitle2, 2, 1, 1, 1)
        spacerItem2 = QSpacerItem(20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.widgetDefenseGridLayout.addItem(spacerItem2, 6, 0, 1, 2)
        self.labelTitle2.setText("算法处理：")

        # 添加调试窗口
        self.textBrowserDebug = QTextBrowser(self)
        self.textBrowserDebug.setMinimumSize(QSize(420, 100))
        self.textBrowserDebug.setMaximumSize(QSize(16777215, 120))
        self.textBrowserDebug.setStyleSheet("QScrollBar:vertical{width:10px;background:rgb(230,235,230);}QScrollBar::handle:vertical{background:rgb(200,200,200);}QTextBrowser{padding: 5px; border:1px solid #e6e6e6;color: rgb(77, 77, 77);}")
        self.textBrowserDebug.setObjectName("textBrowserDebug")
        self.textBrowserDebug.setHtml("")
        self.widgetDefenseGridLayout.addWidget(self.textBrowserDebug, 7, 0, 1, 2)

        # 定义一个读取图像的线程
        self.threadPlay = Thread(self)
        self.threadPlay.console.connect(self.console)
        self.threadPlay.setSourceImage.connect(self.setSourceImage)
        self.threadPlay.setHandleImage.connect(self.setHandleImage)

    # 设置源图像容器点击事件
    def __labelSourceImageClick(self):
        if self.threadPlay.isRun == False:
            self.threadPlay.start()
        else:
            self.clear()

    # 设置处理前的图像
    def setSourceImage(self, image):
        self.labelSourceImage.setPixmap(image)

    # 设置处理后的图像
    def setHandleImage(self, image):
        self.labelHandleImage.setPixmap(image)

    # 清除当前运行的所有进程
    def clear(self, close=False):
        if self.threadPlay.isRun:
            self.threadPlay.isRun = False
            if close:
                self.threadPlay.wait()

    # 输出信息到信息框中
    def console(self, msg):
        self.textBrowserDebug.append(msg)

    # "噪声攻击"按钮点击事件
    def __pushButtonClick(self):
        if self.threadPlay.algorithm:
            self.threadPlay.algorithm = False
            # self.pushButton.setText("噪声攻击")
        else:
            self.threadPlay.algorithm = True
            # self.pushButton.setText("噪声攻击关")