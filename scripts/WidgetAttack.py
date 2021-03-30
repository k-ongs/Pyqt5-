# -*- coding: utf-8 -*-
import cv2
import time
from scripts.scriptsss import cv2ImgAddText
from scripts.QClickLabel import QClickLabel
from PyQt5.QtGui import QPixmap, QImage, QCursor
from PyQt5.QtCore import pyqtSignal,QThread, QSize, Qt
from PyQt5.QtWidgets import QLabel, QWidget, QGridLayout, QSizePolicy, QHBoxLayout, QPushButton, QSpacerItem, QTextBrowser

# 采用线程来播放视频
class Thread(QThread):
    isRun = False
    console = pyqtSignal(str)
    setSourceImage = pyqtSignal(object)
    setHandleImage = pyqtSignal(object)

    def run(self):
        capture = cv2.VideoCapture('data/1-real.avi')
        capture2 = cv2.VideoCapture('data/128P-fullT-2.mp4')
        if not capture.isOpened() or not capture2.isOpened():
            self.console.emit("启动失败！")
            return
        self.isRun = True
        self.console.emit("视频已加载")

        names = ['杨杰之', '彭明杰']
        face_detector = cv2.CascadeClassifier(r'./data/haarcascade_frontalface_default.xml')
        while self.isRun and capture.isOpened():
            ret, frame = capture.read()
            ret2, frame2 = capture2.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)
            faces2 = face_detector.detectMultiScale(gray2, 1.3, 5)

            for (x, y, w, h) in faces:
                # print(x, y, w,h)
                cv2.rectangle(frame, (x, y), (x + w, y + w), (255, 0, 0))
                frame = cv2ImgAddText(frame, names[0], x + 5, y - 30)
            for (x, y, w, h) in faces2:
                cv2.rectangle(frame2, (x, y), (x + w, y + w), (255, 0, 0))
                frame2 = cv2ImgAddText(frame2, names[1], x + 5, y - 30)

            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                rgbImage2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)

                convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
                convertToQtFormat2 = QImage(rgbImage2.data, rgbImage2.shape[1], rgbImage2.shape[0], QImage.Format_RGB888)
                self.setSourceImage.emit(convertToQtFormat)
                self.setHandleImage.emit(convertToQtFormat2)
                time.sleep(0.02)
            else:
                break
        self.isRun = False
        self.setSourceImage.emit(None)
        self.setHandleImage.emit(None)
        self.console.emit("视频已关闭")

class widgetAttack(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        # 定义网格布局
        self.widgetAttackGridLayout = QGridLayout(self)
        self.widgetAttackGridLayout.setContentsMargins(15, 14, 15, 10)
        self.widgetAttackGridLayout.setHorizontalSpacing(10)
        self.widgetAttackGridLayout.setVerticalSpacing(0)
        self.widgetAttackGridLayout.setObjectName("widgetAttackGridLayout")

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
        self.widgetAttackGridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)

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
        self.widgetAttackGridLayout.addWidget(self.labelHandleImage, 5, 1, 1, 1)

        # 添加一个标签显示"处理后："
        self.widgetAttackGridLayout.addWidget(self.labelSourceImage, 5, 0, 1, 1)
        self.labelTitle2 = QLabel(self)
        self.labelTitle2.setMaximumSize(QSize(16777215, 30))
        self.labelTitle2.setStyleSheet("font: 75 13pt \'微软雅黑\';")
        self.labelTitle2.setObjectName("labelTitle2")
        self.widgetAttackGridLayout.addWidget(self.labelTitle2, 2, 1, 1, 1)
        spacerItem2 = QSpacerItem(20, 15, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.widgetAttackGridLayout.addItem(spacerItem2, 6, 0, 1, 2)
        self.labelTitle2.setText("算法处理：")

        # 添加调试窗口
        self.textBrowserDebug = QTextBrowser(self)
        self.textBrowserDebug.setMinimumSize(QSize(420, 100))
        self.textBrowserDebug.setMaximumSize(QSize(16777215, 120))
        self.textBrowserDebug.setStyleSheet("QScrollBar:vertical{width:10px;background:rgb(230,235,230);}QScrollBar::handle:vertical{background:rgb(200,200,200);}QTextBrowser{padding: 5px; border:1px solid #e6e6e6;color: rgb(77, 77, 77);}")
        self.textBrowserDebug.setObjectName("textBrowserDebug")
        self.textBrowserDebug.setHtml("")
        self.widgetAttackGridLayout.addWidget(self.textBrowserDebug, 7, 0, 1, 2)

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
