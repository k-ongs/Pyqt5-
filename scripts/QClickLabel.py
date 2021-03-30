from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, QSize, Qt
from PyQt5.QtWidgets import QWidget, QLabel, QStackedLayout, QSizePolicy

class QClickLabel(QWidget):
    image_show = None
    # 自定义信号
    clicked_signal = pyqtSignal()

    def __init__(self, parent=None):
        super(QClickLabel, self).__init__(parent)
        self.frameShowStackedLayout = QStackedLayout(self)
        self.frameShowStackedLayout.setObjectName("frameShowStackedLayout")
        self.frameShowStackedLayout.setStackingMode(1)

        self.StopBox = QLabel(self)
        self.StopBox.setStyleSheet("background-color: rgba(222, 222, 222, 0);background-image: url(:/system/img/play.png);background-repeat: no-repeat;background-position: center center;")
        self.StopBox.setText("")
        self.frameShowStackedLayout.addWidget(self.StopBox)

        self.ImageBox = QLabel(self)
        self.ImageBox.setStyleSheet("background-color: #242423;")
        self.ImageBox.setText("")

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ImageBox.sizePolicy().hasHeightForWidth())
        self.ImageBox.setSizePolicy(sizePolicy)
        self.ImageBox.setMinimumSize(QSize(200, 200))
        self.ImageBox.setScaledContents(False)
        self.ImageBox.setAlignment(Qt.AlignCenter)

        self.frameShowStackedLayout.addWidget(self.ImageBox)
    
    # 鼠标点击事件
    def mouseReleaseEvent(self, QMouseEvent):
        self.clicked_signal.emit()

    # 可在外部与槽函数连接
    def clicked(self, func):
        self.clicked_signal.connect(func)

    # 格式化图像为当前容器大小
    def __formatImage(self, image):
        w1 = image.width()
        h1 = image.height()
        w2 = self.width()
        h2 = self.height()
        if w1 > h1:
            return image.scaled(w2, w2/w1 * h1, Qt.KeepAspectRatio)
        return image.scaled(h2/h1 * w1, h2, Qt.KeepAspectRatio)

    def setPixmap(self, image):
        if image == None:
            self.frameShowStackedLayout.setCurrentIndex(0)
        else:
            self.image_show = image
            self.frameShowStackedLayout.setCurrentIndex(1)
            self.ImageBox.setPixmap(QPixmap.fromImage(self.__formatImage(image)))

    def resizeEvent(self,event):
        if self.image_show != None:
            self.setPixmap(self.image_show)
            self.setPixmap(None)