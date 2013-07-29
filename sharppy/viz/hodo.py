import numpy as np
from PySide import QtGui, QtCore
import sharppy.sharptab as tab
from sharppy.sharptab.constants import *


__all__ = ['Hodo']


class Hodo(QtGui.QFrame):
    def __init__(self):
        super(Hodo, self).__init__()
        self.initUI()

    def initUI(self):
        '''
        Initialize the User Interface

        '''
        self.lpad = 0; self.rpad = 0
        self.tpad = 0; self.bpad = 0
        self.wid = self.size().width()
        self.hgt = self.size().height()
        self.tlx = self.rpad; self.tly = self.tpad
        self.brx = self.wid; self.bry = self.hgt
        self.centerx = self.wid / 2; self.centery = self.hgt / 2
        self.hodomag = 160; self.hodotop = 15000
        self.scale = (self.brx - self.tlx) / self.hodomag
        self.ring_increment = 10
        self.rings = range(self.ring_increment, 200+self.ring_increment,
                           self.ring_increment)
        self.label_font = QtGui.QFont('Helvetica', 9)

    def resizeEvent(self, e):
        '''
        Resize the plot based on adjusting the main window.

        '''
        self.initUI()

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        for spd in self.rings: self.draw_ring(spd, qp)
        self.draw_axes(qp)
        self.draw_frame(qp)
        qp.end()

    def draw_frame(self, qp):
        '''
        Draw frame around object.

        '''
        pen = QtGui.QPen(QtGui.QColor("#FFFFFF"), 2)
        pen.setStyle(QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(self.tlx, self.tly, self.brx, self.tly)
        qp.drawLine(self.brx, self.tly, self.brx, self.bry)
        qp.drawLine(self.brx, self.bry, self.tlx, self.bry)
        qp.drawLine(self.tlx, self.bry, self.tlx, self.tly)

    def draw_axes(self, qp):
        '''
        Draw the X, Y Axes.

        '''
        pen = QtGui.QPen(QtGui.QColor("#FFFFFF"), 2)
        pen.setStyle(QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(self.centerx, self.tly, self.centerx, self.bry)
        qp.drawLine(self.tlx, self.centery, self.brx, self.centery)

    def draw_ring(self, spd, qp):
        '''
        Draw a range ring.

        '''
        color = "#555555"
        uu, vv = tab.utils.vec2comp(0, spd)
        vv *= self.scale
        center = QtCore.QPointF(self.centerx, self.centery)
        pen = QtGui.QPen(QtGui.QColor(color), 1)
        pen.setStyle(QtCore.Qt.DashLine)
        qp.setPen(pen)
        qp.drawEllipse(center, vv, vv)
        qp.setFont(self.label_font)
        pen = QtGui.QPen(QtGui.QColor('#000000'), 0, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        offset = 5; width = 12; hght = 12;

        top_rect = QtCore.QRectF(self.centerx+offset,
                                 self.centery+vv-offset, width, hght)
        bottom_rect = QtCore.QRectF(self.centerx+offset,
                                    self.centery-vv-offset, width, hght)

        right_rect = QtCore.QRectF(self.centerx+vv-offset,
                                   self.centery+offset, width, hght)
        left_rect = QtCore.QRectF(self.centerx-vv-offset,
                                  self.centery+offset, width, hght)
        qp.drawRect(top_rect); qp.drawRect(right_rect)
        qp.drawRect(bottom_rect); qp.drawRect(left_rect)
        pen = QtGui.QPen(QtGui.QColor("#FFFFFF"))
        qp.setPen(pen)
        qp.setFont(self.label_font)
        qp.drawText(top_rect, QtCore.Qt.AlignCenter, str(int(spd)))
        qp.drawText(right_rect, QtCore.Qt.AlignCenter, str(int(spd)))
        qp.drawText(bottom_rect, QtCore.Qt.AlignCenter, str(int(spd)))
        qp.drawText(left_rect, QtCore.Qt.AlignCenter, str(int(spd)))

    def hodo_to_pix(self, ang, spd):
        '''
        Function to convert a (direction, speed) to (x, y) coordinates.

        '''
        uu, vv = tab.utils.vec2comp(ang, spd)
        xx = self.centerx + (uu * self.scale)
        yy = self.centery + (vv * self.scale)
        return xx, yy

    def uv_to_pix(self, u, v):
        '''
        Function to convert (u, v) to (x, y) coordinates.

        '''
        xx = self.centerx + (u * self.scale)
        yy = self.centery + (v * self.scale)
        return xx, yy
