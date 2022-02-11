# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QPixmap, QColor
from PyQt5.QtCore import Qt, QPoint
from PyQt5 import QtWidgets, QtGui
from PyQt5.uic.properties import QtCore


class Winform(QWidget):
    def __init__(self, parent=None):
        super(Winform, self).__init__(parent)
        # 设置标题
        self.setWindowTitle("地铁漫游")
        # 实例化QPixmap类
        self.pix = QPixmap()
        # 起点，终点
        self.lastPoint = QPoint()
        self.endPoint = QPoint()

        self.X = 1200
        self.Y = 792
        # 初始化
        self.initUi()

    def initUi(self):
        # self.resize(600, 500)  # 窗口大小设置为600*500，这样可以鼠标拖动缩放
        self.setFixedSize(1400, 792)  # 固定窗口大小，不可缩放
        # 画布大小为1200*400，背景为白色
        self.pix = QPixmap("../images/line.png")
        # 偏移量，保证鼠标的位置和画的线点是重合的
        self.offset = QPoint(self.width() - self.pix.width(), self.height() - self.pix.height())

    def clear(self):
        self.pix = QPixmap("../images/line.png")
        self.update()


    def open(self):
        imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", "*.jpg;;*.png;;All Files(*)")
        jpg = QPixmap(imgName).scaled(self.pix.width(), self.pix.height())
        # self.label.setPixmap(jpg)
        self.pix = jpg

    def drawPoint(self,x,y):
        pp = QPainter(self.pix)
        pp.setBrush(QColor(0, 0, 0))
        delatX = 0.005
        delatY = 0.005
        # 根据鼠标指针前后两个位置绘制直线
        pp.drawRoundedRect(int((x / 3000 - delatX) * self.X), int((y / 1978 - delatY) * self.Y),10,10,10,10)

        self.lastPoint = self.endPoint
        painter = QPainter(self)
        # 绘制画布到窗口指定位置处
        painter.drawPixmap(0, 0, self.pix)

    def paintEvent(self, event):
        pp = QPainter(self.pix)
        pp.setBrush(QColor(0,0,0))
        # 根据鼠标指针前后两个位置绘制直线
        # pp.drawRoundedRect(self.endPoint.x(),self.endPoint.y(),10,10,10,10)
        # 让前一个坐标值等于后一个坐标值，
        # 这样就能实现画出连续的线
        self.lastPoint = self.endPoint
        painter = QPainter(self)
        # 绘制画布到窗口指定位置处
        painter.drawPixmap(0, 0, self.pix)


    def mousePressEvent(self, event):
        # 鼠标左键按下
        if event.button() == Qt.LeftButton:
            self.lastPoint = event.pos() - self.offset
            # 上面这里减去一个偏移量，否则鼠标点的位置和线的位置不对齐
            self.endPoint = self.lastPoint


    def mouseMoveEvent(self, event):
        # 鼠标左键按下的同时移动鼠标
        if event.buttons() and Qt.LeftButton:
            self.endPoint = event.pos() - self.offset
            # 进行重新绘制
            self.update()

    def mouseReleaseEvent(self, event):
        # 鼠标左键释放
        if event.button() == Qt.LeftButton:
            self.endPoint = event.pos() - self.offset
            # 进行重新绘制
            self.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = Winform()
    form.show()

    sys.exit(app.exec_())