import numpy as np
from PySide import QtGui, QtCore
import sharppy.sharptab as tab
from sharppy.sharptab.constants import *


__all__ = ['backgroundHodo', 'plotHodo']


class backgroundHodo(QtGui.QFrame):
    def __init__(self):
        super(backgroundHodo, self).__init__()
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
        self.center_hodo()
        self.ring_increment = 10
        self.rings = range(self.ring_increment, 200+self.ring_increment,
                           self.ring_increment)
        self.label_font = QtGui.QFont('Helvetica', 9)

    def center_hodo(self):
        '''
        Center the hodograph in the window. Can/Should be overwritten.

        '''
        self.centerx = self.wid / 2; self.centery = self.hgt / 2
        self.hodomag = 160.
        self.scale = (self.brx - self.tlx) / self.hodomag

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
        offset = 5; width = 15; hght = 15;

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
        yy = self.centery - (v * self.scale)
        return xx, yy




class plotHodo(backgroundHodo):
    def __init__(self, hght, u, v):
        super(plotHodo, self).__init__()
        self.hght = hght
        self.u = u; self.v = v

    def resizeEvent(self, e):
        '''
        Resize the plot based on adjusting the main window.

        '''
        super(plotHodo, self).resizeEvent(e)

    def paintEvent(self, e):
        super(plotHodo, self).paintEvent(e)
        qp = QtGui.QPainter()
        qp.begin(self)
        self.draw_hodo(qp)
        qp.end()

    def draw_hodo(self, qp):
        '''
        Plot the Hodograph.

        '''
        try:
            mask = np.maximum(self.u.mask, self.v.mask)
            z = self.hght[~mask]
            u = self.u[~mask]
            v = self.v[~mask]
        except:
            z = self.hght
            u = self.u
            v = self.v
        xx, yy = self.uv_to_pix(u, v)
        low_level_color = QtGui.QColor("#FF0000")
        mid_level_color = QtGui.QColor("#00FF00")
        upper_level_color = QtGui.QColor("#FFFF00")
        trop_level_color = QtGui.QColor("#00FFFF")
        penwidth = 2
        pen = QtGui.QPen(low_level_color, penwidth)
        pen.setStyle(QtCore.Qt.SolidLine)
        for i in range(xx.shape[0]-1):
            if z[i] < 3000:
                if z[i+1] < 3000:
                    pen = QtGui.QPen(low_level_color, penwidth)
                else:
                    pen = QtGui.QPen(low_level_color, penwidth)
                    tmp_u = tab.interp.generic_interp_hght(3000, z, u)
                    tmp_v = tab.interp.generic_interp_hght(3000, z, v)
                    tmp_x, tmp_y = self.uv_to_pix(tmp_u, tmp_v)
                    qp.drawLine(xx[i], yy[i], tmp_x, tmp_y)
                    pen = QtGui.QPen(mid_level_color, penwidth)
                    qp.setPen(pen)
                    qp.drawLine(tmp_x, tmp_y, xx[i+1], yy[i+1])
                    continue
            elif z[i] < 6000:
                if z[i+1] < 6000:
                    pen = QtGui.QPen(mid_level_color, penwidth)
                else:
                    pen = QtGui.QPen(mid_level_color, penwidth)
                    tmp_u = tab.interp.generic_interp_hght(6000, z, u)
                    tmp_v = tab.interp.generic_interp_hght(6000, z, v)
                    tmp_x, tmp_y = self.uv_to_pix(tmp_u, tmp_v)
                    qp.drawLine(xx[i], yy[i], tmp_x, tmp_y)
                    pen = QtGui.QPen(upper_level_color, penwidth)
                    qp.setPen(pen)
                    qp.drawLine(tmp_x, tmp_y, xx[i+1], yy[i+1])
                    continue
            elif z[i] < 9000:
                if z[i+1] < 9000:
                    pen = QtGui.QPen(upper_level_color, penwidth)
                else:
                    pen = QtGui.QPen(upper_level_color, penwidth)
                    tmp_u = tab.interp.generic_interp_hght(9000, z, u)
                    tmp_v = tab.interp.generic_interp_hght(9000, z, v)
                    tmp_x, tmp_y = self.uv_to_pix(tmp_u, tmp_v)
                    qp.drawLine(xx[i], yy[i], tmp_x, tmp_y)
                    pen = QtGui.QPen(trop_level_color, penwidth)
                    qp.setPen(pen)
                    qp.drawLine(tmp_x, tmp_y, xx[i+1], yy[i+1])
                    continue
            elif z[i] < 12000:
                if z[i+1] < 12000:
                    pen = QtGui.QPen(trop_level_color, penwidth)
                else:
                    pen = QtGui.QPen(low_level_color, penwidth)
                    tmp_u = tab.interp.generic_interp_hght(12000, z, u)
                    tmp_v = tab.interp.generic_interp_hght(12000, z, v)
                    tmp_x, tmp_y = self.uv_to_pix(tmp_u, tmp_v)
                    qp.drawLine(xx[i], yy[i], tmp_x, tmp_y)
                    break
            else:
                break
            qp.setPen(pen)
            qp.drawLine(xx[i], yy[i], xx[i+1], yy[i+1])
