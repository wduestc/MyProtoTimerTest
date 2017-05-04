# -*- coding: gb18030 -*-
import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtCore import SIGNAL as signal


#pyqt4中文化处理 使用默认的
QTextCodec.setCodecForTr(QTextCodec.codecForName("system"))
QTextCodec.setCodecForCStrings(QTextCodec.codecForName("system"))
QTextCodec.setCodecForLocale(QTextCodec.codecForName("system"))

class LcdTime(QtGui.QFrame):
    def __init__(self, parent=None):
        super(LcdTime, self).__init__(parent)
        self.hour = QtGui.QLCDNumber(8, self)
        self.hour.setGeometry(10, 10, 200, 70)
        self.hour.setSegmentStyle(QtGui.QLCDNumber.Flat)
        self.display()
        self.timer = QtCore.QTimer()
        self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.display)
        self.timer.start(1000)
        #建立一个托盘用于特殊处理
        #实际上应该重新点击后重新进行计时处理
        self.build_tray()
        self.resize(220, 100)
        self.central()
        # 边框透明
        self.hour.setFrameShape(QtGui.QFrame.NoFrame)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.SubWindow | QtCore.Qt.WindowStaysOnTopHint)
        # 透明处理，移动需要拖动数字
        #self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setMouseTracking(True)

        #设置弹出菜单
        #设置一个Quit的标签
        quitAction = QtGui.QAction('&Quit', self)
        self.connect(quitAction, signal("triggered()"), QtGui.qApp.quit)
        setAction = QtGui.QAction('&Setting', self)
        #添加子菜单
        scaleMenu = QtGui.QMenu()
        setAction.setMenu(scaleMenu)
        StartScaleAction = QtGui.QAction('&开始',  self)
        StopScaleAction = QtGui.QAction('&暂停',   self)
        EndScaleAction  = QtGui.QAction('&终止',   self)
        scaleMenu.addAction(StartScaleAction)
        scaleMenu.addAction(StopScaleAction)
        scaleMenu.addAction(EndScaleAction)

        #self.connect(setAction,  signal("triggered()"), self.scaleMenu)
        #backAction = QtGui.QAction('&Back', self)
        #self.connect(backAction, signal("triggered()"), self.backClicked)
        self.popMenu = QtGui.QMenu()
        self.popMenu.addAction(quitAction)
        self.popMenu.addAction(setAction)
        #self.popMenu.addAction(backAction)

    #鼠标点击事件
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
        if event.button() == QtCore.Qt.RightButton:
            self.rightButton = True

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()

    #鼠标右键事件
    def mouseReleaseEvent(self, e):
        if self.rightButton == True:
            self.rightButton = False
            self.popMenu.popup(e.globalPos())

    #创建子菜单

    #系统托盘,需要logo.png
    def build_tray(self):
        self.trayIcon = QtGui.QSystemTrayIcon(self)
        self.trayIcon.setIcon(QtGui.QIcon('logo.png'))
        self.trayIcon.show()
        self.trayIcon.setToolTip('时钟 -LiKui')
        self.trayIcon.activated.connect(self.trayClick)
        menu = QtGui.QMenu()
        normalAction = menu.addAction('正常显示')
        miniAction = menu.addAction('最小化托盘')
        exitAction = menu.addAction('退出')
        normalAction.triggered.connect(self.showNormal)
        exitAction.triggered.connect(self.exit)
        miniAction.triggered.connect(self.showMinimized)
        self.trayIcon.setContextMenu(menu)
    def exit(self):
        # 不设置Visible为False，退出后TrayIcon不会刷新
        self.trayIcon.setVisible(False)
        sys.exit(0)
    def trayClick(self, reason):
        if reason == QtGui.QSystemTrayIcon.DoubleClick:
            self.showNormal()
            self.repaint()
    def display(self):
        current = QtCore.QTime.currentTime()
        self.hour.display(current.toString('HH:mm:ss'))
    def showNormal(self):
        super(LcdTime, self).showNormal()
        self.repaint()
    def central(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move(screen.width() - size.width(), 0)

app = QtGui.QApplication(sys.argv)
lcd = LcdTime()
lcd.show()
sys.exit(app.exec_())