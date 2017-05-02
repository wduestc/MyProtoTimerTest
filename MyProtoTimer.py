# -*- coding: utf-8 -*-
"""
方法名称:MyProtoTimer.py
方法功能:随机选择+自动计时
创建日期:2017.4.29
创建者:w_di_sc
"""
import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *

QTextCodec.setCodecForTr(QTextCodec.codecForName("system"))
QTextCodec.setCodecForCStrings(QTextCodec.codecForName("system"))
QTextCodec.setCodecForLocale(QTextCodec.codecForName("system"))

"""
使用git进行提交 同时提交GitHub
"""
class MyProto(QtGui.QWidget):
    def __init__(self):
        super(MyProto, self).__init__()
        self.initUI()
    def initUI(self):

        self.readerAuthor = QtGui.QLabel('')
        self.readerTimer = QtGui.QLabel('')
        self.readerAuthor.setFont(QFont("Roman times", 25, QFont.Bold))
        self.readerAuthor.setAlignment(Qt.AlignCenter)

        self.readerTimer.setFont(QFont("Roman times", 25, QFont.Bold))
        self.readerTimer.setAlignment(Qt.AlignCenter)
        #titleEdit = QtGui.QLineEdit()
        #authorEdit = QtGui.QLineEdit()
        reviewEdit = QtGui.QTextEdit()
        grid = QtGui.QGridLayout()

        grid.setRowStretch(1, 10)
        grid.setColumnStretch(10, 1 )
        grid.setSpacing(10)

        btn1Choice = QtGui.QPushButton("随机抽取".decode("utf-8").encode("gb18030"))
        btn1Choice.clicked.connect(self.ChoiceItem)
        #btn2Choice = QtGui.QPushButton("")
        btn1 = QtGui.QPushButton("开始计时".decode("utf-8").encode("gb18030"))
        btn2 = QtGui.QPushButton("停止".decode("utf-8").encode("gb18030"))
        btn3 = QtGui.QPushButton("重新计时".decode("utf-8").encode("gb18030"))
        btn1.clicked.connect(self.buttonTimerStart)
        btn2.clicked.connect(self.buttonTimerEnd)
        btn3.clicked.connect(self.buttonReTimerStart)


        """
        self.lcd = QtGui.QLCDNumber(self)
        self.lcd.setDigitCount(10)
        #窗体透明
        self.lcd.setFrameShape(QtGui.QFrame.NoFrame)
        self.lcd.setMode(QtGui.QLCDNumber.Dec)
        self.lcd.setSegmentStyle(QtGui.QLCDNumber.Flat)
        """
        self.showColon = True
        self.TimerRunning = False
        self.global_hours = 0
        self.global_minutes = 0
        self.global_seconds = 0

        #获取
        self.global_choice_items = []
        """
        #self.init_time = "%02d:%02d:%02d" % (self.global_hours, self.global_minutes, self.global_seconds)
        self.init_time = "%02d:%02d" % (self.global_minutes, self.global_seconds)
        """
        grid.addWidget(btn1Choice, 0, 0)
        grid.addWidget(btn1, 0, 1)
        grid.addWidget(btn2, 0, 2)
        grid.addWidget(btn3, 0, 3)

        #重置grid
        grid.addWidget(self.readerTimer, 1, 2, 1, 20)
        grid.addWidget(self.readerAuthor,1, 0, 1, 10)

        #设置背景图案

        palette1 = QtGui.QPalette()
        #这里跟系统分辨率有关系
        screen = QtGui.QDesktopWidget().screenGeometry()
        jpeg = QtGui.QPixmap("timg.jpg").scaled(screen.width(), screen.height())
        #jpeg.load("test1.bmp")
        palette1.setBrush(self.backgroundRole(), QtGui.QBrush(jpeg))
        #palette1.setColor(self.backgroundRole(), QtGui.QBrush())
        self.setPalette(palette1)

        
        #self.setAutoFillBackground(True)
        self.setLayout(grid)
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('计时器'.decode("utf-8").encode("gb18030"))
        self.show()
        #self.setWindowFlags(Qt.FramelessWindowHint)
        #self.showFullScreen()

    def ChoiceItem(self):
        if len(self.global_choice_items) == 0:
            fileName="ChoiceItemBefore.txt"
            with open(fileName, "r") as fp_read:
                for line in fp_read.readlines():
                    self.global_choice_items.append(line.strip())

        from random import choice
        choice_simple_item = choice(self.global_choice_items)
        self.readerAuthor.setText(choice_simple_item.decode("utf-8").encode("gb18030"))
        self.global_choice_items.remove(choice_simple_item)
            #print choice_simple_item





    def buttonReTimerStart(self):
        self.timer.stop()
        self.global_hours = 0
        self.global_minutes = 0
        self.global_seconds = 0
        self.init_time = "%02d:%02d" % (self.global_minutes, self.global_seconds)
        self.readerTimer.setText(self.init_time)
        #self.lcd.display(self.init_time)
        self.buttonTimerStart()

    def buttonTimerEnd(self):
        if self.TimerRunning == True:
          self.timer.stop()
        #self.global_hours = 0
        #self.global_minutes = 0
        #self.global_seconds = 0
        self.init_time = "%02d:%02d" % (self.global_minutes, self.global_seconds)
        self.readerTimer.setText(self.init_time)
        #self.lcd.display(self.init_time)

    def buttonTimerStart(self):
        self.timer = QTimer(self)
        #self.count = 0
        freq_time = 100
        self.timer.start(freq_time)
        self.TimerRunning = True
        self.connect(self.timer, SIGNAL("timeout()"), self.showTime)

    def showTime(self):
        self.global_seconds += 1
        if self.global_seconds == 60:
            self.global_minutes +=1
            self.global_seconds = 0
        if self.global_minutes == 60:
            self.global_hours +=1
            self.global_minutes = 0
            self.global_seconds = 0
        #判断如果到达规定的时间则需要进行提示
        #if self.global_minutes == 5:
        """
        if self.global_minutes == 1 and self.global_seconds == 1:
            #已经达到5
            QtGui.QMessageBox.information(self, "友情提示".decode("utf-8").encode("gb18030"), "时间到".decode("utf-8").encode("gb18030"))
        """
        text="%02d:%02d"%(self.global_minutes, self.global_seconds)
        #self.lcd.display(text)
        self.readerTimer.setText(text)
        if self.global_minutes == 1 and self.global_seconds == 0:
            #已经达到5
            #TODO 可以继续加载其他的需求
            QtGui.QMessageBox.information(self, "友情提示".decode("utf-8").encode("gb18030"), "时间到".decode("utf-8").encode("gb18030"))
def main():
    app = QtGui.QApplication(sys.argv)
    ex = MyProto()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()