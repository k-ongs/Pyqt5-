# -*- coding: utf-8 -*-
import sys
import collections
from data import resources
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QMouseEvent, QIcon
from scripts.window_effect import WindowEffect
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, QPropertyAnimation,QPoint

from scripts.WidgetAttack import widgetAttack
from scripts.WidgetDefense import widgetDefense
from scripts.WidgetBioassay import widgetBioassay

# 窗体主体
class MainForm(QWidget):
    # 移动标识符
    __move_flag = False
    # 当前选中菜单
    __menu_index = 0
    # 菜单列表
    __menu_list = []
    # 有序字典
    __menu_labels = collections.OrderedDict()
    # 显示控件列表
    __frame_list = collections.OrderedDict()

    # 初始化窗体
    def __init__(self, menu_list):
        # 添加菜单项
        self.__menu_list = menu_list
        # 设置为顶级窗口，无边框
        super(MainForm, self).__init__(None, Qt.FramelessWindowHint)
        # 设置窗体大小
        self.resize(710, 500)
        # 为窗口添加阴影
        self.windowEffect = WindowEffect()
        self.windowEffect.addShadowEffect(self.winId())
        # 设置窗体最小尺寸
        # self.setMinimumSize(QtCore.QSize(550, 400))
        self.setMinimumSize(QtCore.QSize(700, 500))
        # 设置程序标题
        self.setWindowTitle("调试程序")
        # 设置程序图标
        self.setWindowIcon(QIcon('data/img/favicon.ico'))
        # 设置为无边框
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 设置背景颜色
        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        # 添加QGridLayout布局
        self.FormGridLayout = QtWidgets.QGridLayout(self)
        self.FormGridLayout.setContentsMargins(0, 0, 0, 0)
        self.FormGridLayout.setSpacing(0)
        self.FormGridLayout.setObjectName("FormGridLayout")

        # 初始化控件
        self.__setTopLabel()
        self.__setFrameShow()
        self.__setLeftLabel()
        # 显示窗体
        self.show()

    # 设置顶部控制栏容器
    def __setTopLabel(self):
        self.widgetTop = QtWidgets.QWidget(self)
        self.widgetTop.setMinimumSize(QtCore.QSize(450, 31))
        self.widgetTop.setMaximumSize(QtCore.QSize(16777215, 31))
        self.widgetTop.setStyleSheet("background-color: rgb(255, 255, 255);border-bottom:1px solid rgb(230, 230, 230);")
        self.widgetTop.setObjectName("widgetTop")

        # 添加一个QHBoxLayout布局
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widgetTop)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # 添加控制栏标题和按钮
        self.__setTopLabelButtons()

        # 将控制栏添加到窗体
        self.FormGridLayout.addWidget(self.widgetTop, 0, 1, 1, 1)

    # 设置控制栏按钮
    def __setTopLabelButtons(self):
        # 添加公告信息
        self.notice = QtWidgets.QLabel(self.widgetTop)
        self.notice.setMinimumSize(QtCore.QSize(0, 30))
        self.notice.setMaximumSize(QtCore.QSize(16777215, 30))
        self.notice.setStyleSheet("padding-left:5px; border:none;")
        self.notice.setFrameShape(QtWidgets.QFrame.Panel)
        self.notice.setFrameShadow(QtWidgets.QFrame.Raised)
        self.notice.setLineWidth(0)
        self.notice.setText("")
        self.notice.setObjectName("notice")
        self.horizontalLayout.addWidget(self.notice)

        # 添加最小化按钮
        self.minimizeButton = QtWidgets.QPushButton(self.widgetTop)
        self.minimizeButton.setMinimumSize(QtCore.QSize(30, 30))
        self.minimizeButton.setMaximumSize(QtCore.QSize(30, 30))
        self.minimizeButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.minimizeButton.setStyleSheet("QPushButton{background-color: rgba(0, 0, 0, 0); border-image: url(:/system/img/minimize.png);}QPushButton::hover{background-color: rgba(240, 240, 240, 255);}")
        self.minimizeButton.setText("")
        self.minimizeButton.setObjectName("minimizeButton")
        self.minimizeButton.clicked.connect(self.showMinimized)

        self.horizontalLayout.addWidget(self.minimizeButton)

        # 添加最大化按钮
        self.maximizeButton = QtWidgets.QPushButton(self.widgetTop)
        self.maximizeButton.setMinimumSize(QtCore.QSize(30, 30))
        self.maximizeButton.setMaximumSize(QtCore.QSize(30, 30))
        self.maximizeButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.maximizeButton.setStyleSheet("QPushButton{background-color: rgba(0, 0, 0, 0); border-image: url(:/system/img/maximize.png);}QPushButton::hover{background-color: rgba(240, 240, 240, 255);}")
        self.maximizeButton.setText("")
        self.maximizeButton.setObjectName("maximizeButton")
        self.maximizeButton.clicked.connect(self.__showMaximizedBox)
        self.horizontalLayout.addWidget(self.maximizeButton)

        # 添加关闭按钮
        self.closeButton = QtWidgets.QPushButton(self.widgetTop)
        self.closeButton.setMinimumSize(QtCore.QSize(30, 30))
        self.closeButton.setMaximumSize(QtCore.QSize(30, 30))
        self.closeButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.closeButton.setStyleSheet("QPushButton{border-image: url(:/system/img/close.png);} QPushButton::hover{border-image: url(:/system/img/close_hover.png);}")
        self.closeButton.setText("")
        self.closeButton.setObjectName("closeButton")
        self.closeButton.clicked.connect(self.close)
        self.horizontalLayout.addWidget(self.closeButton)

    # 设置左边菜单背景
    def __setLeftLabel(self):
        self.widgetLeft = QtWidgets.QWidget(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widgetLeft.sizePolicy().hasHeightForWidth())
        self.widgetLeft.setSizePolicy(sizePolicy)
        self.widgetLeft.setMinimumSize(QtCore.QSize(140, 400))
        self.widgetLeft.setMaximumSize(QtCore.QSize(140, 16777215))
        self.widgetLeft.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.widgetLeft.setStyleSheet("background-color: qlineargradient(spread:reflect, x1:0.5, y1:0, x2:0.5, y2:1, stop:0 rgba(38, 112, 234, 255), stop:1 rgba(62, 132, 254, 255));")
        self.widgetLeft.setObjectName("widgetLeft")
        self.widgetLeftVerticalLayout = QtWidgets.QVBoxLayout(self.widgetLeft)
        self.widgetLeftVerticalLayout.setContentsMargins(0, 0, 0, 0)
        self.widgetLeftVerticalLayout.setSpacing(1)
        self.widgetLeftVerticalLayout.setObjectName("widgetLeftVerticalLayout")

        # 设置程序标题
        self.titleLabel = QtWidgets.QLabel(self.widgetLeft)
        self.titleLabel.setMinimumSize(QtCore.QSize(140, 30))
        self.titleLabel.setMaximumSize(QtCore.QSize(140, 30))
        self.titleLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.titleLabel.setStyleSheet("background-color: rgba(0, 0, 0, 0); font: 12pt \'微软雅黑\'; color: rgb(255, 255, 255);padding-left:10px;")
        self.titleLabel.setFrameShadow(QtWidgets.QFrame.Plain)
        self.titleLabel.setAlignment(QtCore.Qt.AlignVCenter)
        self.titleLabel.setObjectName("titleLabel")
        self.titleLabel.setText("调试程序")
        self.widgetLeftVerticalLayout.addWidget(self.titleLabel)
        
        # 添加菜单项
        self.__setMenuLeble()

        # 将菜单栏添加到窗体
        self.FormGridLayout.addWidget(self.widgetLeft, 0, 0, 3, 1)

    # 设置菜单项
    def __setMenuLeble(self):
        # 添加QSpacerItem弹簧占位
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.widgetLeftVerticalLayout.addItem(spacerItem)

        # 添加菜单项
        for name, example in self.__menu_list.items():
            # 初始化对应视图
            self.__frame_list[name] = example(self.frameShow)
            # 将视图添加到显示容器中
            self.frameShowStackedLayout.addWidget(self.__frame_list[name])

            # 创建一个单选按钮
            self.__menu_labels[name] = QtWidgets.QRadioButton(self.widgetLeft)
            # 设置最小尺寸
            self.__menu_labels[name].setMinimumSize(QtCore.QSize(100, 42))
            # 设置最大尺寸
            self.__menu_labels[name].setMaximumSize(QtCore.QSize(16777215, 42))
            # 设置鼠标样式
            self.__menu_labels[name].setCursor(QtGui.QCursor(Qt.PointingHandCursor))
            # 设置样式
            self.__menu_labels[name].setStyleSheet("QRadioButton{background: rgba(0, 0, 0, 0) url(:/system/img/menu_icon_" + self.__frame_list[name].__class__.__name__ + ".png) no-repeat left center;color: rgb(255, 255, 255);font: 75 10pt \'微软雅黑\';}QRadioButton::checked,QRadioButton::hover{background-color: rgba(89, 146, 244, 255);}QRadioButton::indicator {width: 46px;height: 1px;background-color: rgba(0, 0, 0, 0);}")
            # 设置显示文本
            self.__menu_labels[name].setText(name)
            # 绑定事件
            self.__menu_labels[name].toggled.connect(lambda:self.__radioButtonToggled(self.sender().text()))

            # 将此菜单项添加到菜单容器里面
            self.widgetLeftVerticalLayout.addWidget(self.__menu_labels[name])

        # 默认选中第一个菜单
        list(self.__menu_labels.values())[0].setChecked(True)

        # 添加QSpacerItem弹簧占位
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.widgetLeftVerticalLayout.addItem(spacerItem1)

    # 添加显示容器
    def __setFrameShow(self):
        # 创建一个QFrame容器
        self.frameShow = QtWidgets.QFrame(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameShow.sizePolicy().hasHeightForWidth())
        self.frameShow.setSizePolicy(sizePolicy)
        # 设置最小尺寸
        self.frameShow.setMinimumSize(QtCore.QSize(450, 369))
        self.frameShow.setStyleSheet("background-color: rgb(255, 255, 255);border:none;")
        self.frameShow.setFrameShape(QtWidgets.QFrame.Panel)
        self.frameShow.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameShow.setObjectName("frameShow")
        # 添加QStackedLayout, 实现页面切换
        self.frameShowStackedLayout = QtWidgets.QStackedLayout(self.frameShow)
        self.frameShowStackedLayout.setObjectName("frameShowStackedLayout")
        self.frameShowStackedLayout.setStackingMode(1)
        # 将此容器添加到窗体
        self.FormGridLayout.addWidget(self.frameShow, 1, 1, 1, 1)

    # 菜单状态更改事件
    def __radioButtonToggled(self, name):
        if self.__menu_labels[name].isChecked():
            # 切换到对应页面
            _this_id = list(self.__menu_labels.keys()).index(name)

            self.frameShowStackedLayout.setCurrentIndex(_this_id)
            if _this_id != self.__menu_index:
                _old_name = list(self.__menu_labels.keys())[self.__menu_index]
                self.animation_1 = QPropertyAnimation(self.__frame_list[name], b'pos')
                self.animation_2 = QPropertyAnimation(self.__frame_list[_old_name], b'pos')
                self.animation_1.setDuration(300)
                self.animation_2.setDuration(300)

                if _this_id > self.__menu_index:
                    self.animation_1.setStartValue(QPoint(0, self.__frame_list[name].height()))
                    self.animation_2.setEndValue(QPoint(0, -self.__frame_list[name].height()))
                else:
                    self.animation_1.setStartValue(QPoint(0, -self.__frame_list[name].height()))
                    self.animation_2.setEndValue(QPoint(0, self.__frame_list[name].height()))

                self.animation_1.setEndValue(QPoint(0, 0))
                self.animation_2.setStartValue(QPoint(0, 0))

                self.animation_1.start()
                self.animation_2.start()

            self.__menu_index = _this_id
            self.__menu_labels[name].setCursor(QtGui.QCursor(Qt.ArrowCursor))
        else:
            # 此模块关闭, 停止相应进程
            self.__frame_list[name].clear()
            self.__menu_labels[name].setCursor(QtGui.QCursor(Qt.PointingHandCursor))

    # 最大化与复原
    def __showMaximizedBox(self):    
        if self.isMaximized():
            self.showNormal()
            self.maximizeButton.setStyleSheet("QPushButton{background-color: rgba(0, 0, 0, 0); border-image: url(:/system/img/maximize.png);}QPushButton::hover{background-color: rgba(240, 240, 240, 255);}")
        else:
            self.showMaximized()
            self.maximizeButton.setStyleSheet("QPushButton{background-color: rgba(0, 0, 0, 0); border-image: url(:/system/img/reduction.png);}QPushButton::hover{background-color: rgba(240, 240, 240, 255);}")

    # 鼠标点击事件
    def mousePressEvent(self, event):
        # 鼠标在控制栏区域才能移动
        if (event.button() == Qt.LeftButton) and (event.y() < self.widgetTop.height()):
            # 鼠标左键点击标题栏区域
            self.__move_flag = True
            self.move_DragPosition = event.globalPos() - self.pos()
            event.accept()

    # 鼠标移动事件
    def mouseMoveEvent(self, QMouseEvent):
        # 鼠标在控制栏区域才能移动
        if Qt.LeftButton and self.__move_flag:
            self.move(QMouseEvent.globalPos() - self.move_DragPosition)
            QMouseEvent.accept()

    # 鼠标释放事件
    def mouseReleaseEvent(self, e: QMouseEvent):
        self.__move_flag = False

    # 程序关闭事件
    def closeEvent(self, event):
        for frame_temp in self.__frame_list.values():
            frame_temp.clear(True)

if __name__ == '__main__':
    menu_list = {'活体检测': widgetBioassay, '换脸': widgetAttack, '对抗攻击': widgetDefense}
    app = QApplication(sys.argv)
    ui = MainForm(menu_list)
    sys.exit(app.exec_())