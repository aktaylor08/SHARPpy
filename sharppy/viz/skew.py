import numpy as np
import sharppy.sharptab as tab
from sharppy.sharptab.constants import *
from PySide import QtGui, QtCore


__all__ = ['backgroundSkewT', 'plotSkewT']

class backgroundSkewT(QtGui.QFrame):
    def __init__(self):
        super(backgroundSkewT, self).__init__()
        self.initUI()

    def initUI(self):
        '''
        Initialize the User Interface.

        '''
        self.lpad = 30; self.rpad = 50
        self.tpad = 20; self.bpad = 20
        self.wid = self.size().width() - self.rpad
        self.hgt = self.size().height() - self.bpad
        self.brx = self.wid ; self.bry = self.hgt
        self.pmax = 1050.; self.pmin = 100.
        self.barbx = self.brx + self.rpad / 2
        self.log_pmax = np.log(1050.); self.log_pmin = np.log(self.pmin)
        self.bltmpc = -50; self.brtmpc = 50; self.dt = 10
        self.xskew = 100 / 3.
        self.xrange = self.brtmpc - self.bltmpc
        self.yrange = np.tan(np.deg2rad(self.xskew)) * self.xrange
        self.label_font = QtGui.QFont('Helvetica', 11)
        self.environment_trace_font = QtGui.QFont('Helvetica', 11)
        self.in_plot_font = QtGui.QFont('Helvetica', 7)

    def resizeEvent(self, e):
        '''
        Resize the plot based on adjusting the main window.

        '''
        self.initUI()

    def paintEvent(self, e):
        '''
        Draw the background features of a Skew-T.

        '''
        qp = QtGui.QPainter()
        qp.begin(self)
        for t in range(self.bltmpc-100, self.brtmpc+self.dt+100, self.dt):
            self.draw_isotherm(t, qp)
        for tw in range(-160, 61, 10): self.draw_moist_adiabat(tw, qp)
        for theta in range(-70, 350, 20): self.draw_dry_adiabat(theta, qp)
        for w in [2] + range(4, 33, 4): self.draw_mixing_ratios(w, 600, qp)
        self.draw_frame(qp)
        for p in [1000, 850, 700, 500, 300, 200, 100]:
            self.draw_isobar(p, 1, qp)
        for t in range(self.bltmpc, self.brtmpc+self.dt, self.dt):
            self.draw_isotherm_labels(t, qp)
        for p in range(int(self.pmax), int(self.pmin-50), -50):
            self.draw_isobar(p, 0, qp)
        qp.end()

    def draw_dry_adiabat(self, theta, qp):
        '''
        Draw the given moist adiabat.

        '''
        pen = QtGui.QPen(QtGui.QColor("#333333"), 1)
        pen.setStyle(QtCore.Qt.SolidLine)
        qp.setPen(pen)
        dt = -10
        presvals = np.arange(int(self.pmax), int(self.pmin)+dt, dt)
        thetas = tab.thermo.theta(presvals, theta)
        thetas = ((theta + ZEROCNK) / ((1000. / presvals)**ROCP)) - ZEROCNK
        for t, p in zip(thetas, presvals):
            x = self.tmpc_to_pix(t, p)
            y = self.pres_to_pix(p)
            if p == self.pmax:
                x2 = x; y2 = y
            else:
                x1 = x2; y1 = y2
                x2 = x; y2 = y
                qp.drawLine(x1, y1, x2, y2)

    def draw_moist_adiabat(self, tw, qp):
        '''
        Draw the given moist adiabat.

        '''
        pen = QtGui.QPen(QtGui.QColor("#663333"), 1)
        pen.setStyle(QtCore.Qt.SolidLine)
        qp.setPen(pen)
        dt = -10
        for p in range(int(self.pmax), int(self.pmin)+dt, dt):
            t = tab.thermo.wetlift(1000., tw, p)
            x = self.tmpc_to_pix(t, p)
            y = self.pres_to_pix(p)
            if p == self.pmax:
                x2 = x; y2 = y
            else:
                x1 = x2; y1 = y2
                x2 = x; y2 = y
                qp.drawLine(x1, y1, x2, y2)

    def draw_mixing_ratios(self, w, pmin, qp):
        '''
        Draw the mixing ratios.

        '''
        t = tab.thermo.temp_at_mixrat(w, self.pmax)
        x1 = self.tmpc_to_pix(t, self.pmax)
        y1 = self.pres_to_pix(self.pmax)
        t = tab.thermo.temp_at_mixrat(w, pmin)
        x2 = self.tmpc_to_pix(t, pmin)
        y2 = self.pres_to_pix(pmin)
        rectF = QtCore.QRectF(x2-5, y2-10, 10, 10)
        pen = QtGui.QPen(QtGui.QColor('#000000'), 1, QtCore.Qt.SolidLine)
        brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
        qp.setPen(pen)
        qp.setBrush(brush)
        qp.drawRect(rectF)
        pen = QtGui.QPen(QtGui.QColor('#006600'), 1, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.setFont(self.in_plot_font)
        qp.drawLine(x1, y1, x2, y2)
        qp.drawText(rectF, QtCore.Qt.AlignBottom | QtCore.Qt.AlignCenter,
            str(int(w)))

    def draw_frame(self, qp):
        '''
        Draw the frame around the Skew-T.

        '''
        pen = QtGui.QPen(QtGui.QColor('#000000'), 0, QtCore.Qt.SolidLine)
        brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
        qp.setPen(pen)
        qp.setBrush(brush)
        qp.drawRect(0, 0, self.lpad, self.bry)
        qp.drawRect(0, self.pres_to_pix(self.pmax), self.brx, self.bry)
        qp.drawRect(self.brx, 0, self.wid+self.rpad,
                    self.pres_to_pix(self.pmax))
        pen = QtGui.QPen(QtCore.Qt.white, 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(self.lpad, self.tpad, self.brx+self.rpad, self.tpad)
        qp.drawLine(self.brx+self.rpad, self.tpad, self.brx+self.rpad,
                    self.bry)
        qp.drawLine(self.brx+self.rpad, self.bry, self.lpad, self.bry)
        qp.drawLine(self.lpad, self.bry, self.lpad, self.tpad)

    def draw_isotherm_labels(self, t, qp):
        '''
        Add Isotherm Labels.

        '''
        pen = QtGui.QPen(QtGui.QColor("#FFFFFF"))
        qp.setFont(self.label_font)
        x1 = self.tmpc_to_pix(t, self.pmax)
        qp.drawText(x1-10, self.bry+2, 20, 20,
                    QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter, str(int(t)))

    def draw_isotherm(self, t, qp):
        '''
        Draw background isotherms.

        '''
        x1 = self.tmpc_to_pix(t, self.pmax)
        x2 = self.tmpc_to_pix(t, self.pmin)
        if t in [0, -20]:
            pen = QtGui.QPen(QtGui.QColor("#0000FF"), 1)
        else:
            pen = QtGui.QPen(QtGui.QColor("#555555"), 1)
        pen.setStyle(QtCore.Qt.CustomDashLine)
        pen.setDashPattern([4, 2])
        qp.setPen(pen)
        qp.drawLine(x1, self.bry, x2, self.tpad)

    def draw_isobar(self, p, flag, qp):
        '''
        Draw background isobars.

        '''
        pen = QtGui.QPen(QtGui.QColor("#FFFFFF"), 1, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.setFont(self.label_font)
        y1 = self.pres_to_pix(p)
        offset = 5
        if flag:
            qp.drawLine(self.lpad, y1, self.brx, y1)
            qp.drawText(0, y1-20, self.lpad-4, 40,
                        QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight,
                        str(int(p)))
        else:
            qp.drawLine(self.lpad, y1, self.lpad+offset, y1)
            qp.drawLine(self.brx+self.rpad-offset, y1,
                        self.brx+self.rpad, y1)

    def tmpc_to_pix(self, t, p):
        '''
        Function to convert a (temperature, pressure) coordinate
        to an X pixel.

        '''
        scl1 = self.brtmpc - (((self.bry - self.pres_to_pix(p)) /
                              (self.bry - self.tpad)) * self.yrange)
        return self.brx - (((scl1 - t) / self.xrange) * (self.brx - self.lpad))

    def pres_to_pix(self, p):
        '''
        Function to convert a pressure value (level) to a Y pixel.

        '''
        scl1 = self.log_pmax - self.log_pmin
        scl2 = self.log_pmax - np.log(p)
        return self.bry - (scl2 / scl1) * (self.bry - self.tpad)

    def pix_to_pres(self, y):
        '''
        Function to convert a Y pixel to a pressure level.

        '''
        scl1 = np.log(self.pmax) - np.log(self.pmin)
        scl2 = self.bry - float(y)
        scl3 = self.bry - self.tly + 1
        return self.pmax / np.exp((scl2 / scl3) * scl1)




class plotSkewT(backgroundSkewT):
    def __init__(self, pres, hght, tmpc, dwpc):
        super(plotSkewT, self).__init__()
        self.pres = pres; self.hght = hght
        self.tmpc = tmpc; self.dwpc = dwpc

    def resizeEvent(self, e):
        '''
        Resize the plot based on adjusting the main window.

        '''
        super(plotSkewT, self).resizeEvent(e)

    def paintEvent(self, e):
        '''
        Plot the data used in a Skew-T.

        '''
        super(plotSkewT, self).paintEvent(e)
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawTrace(self.dwpc, QtGui.QColor("#00FF00"), qp)
        self.drawTrace(self.tmpc, QtGui.QColor("#FF0000"), qp)
        qp.end()

    def drawTrace(self, data, color, qp):
        '''
        Draw an environmental trace.

        '''
        pen = QtGui.QPen(QtGui.QColor(color), 3, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        mask1 = data.mask
        mask2 = self.pres.mask
        mask = np.maximum(mask1, mask2)
        data = data[~mask]
        pres = self.pres[~mask]
        x = self.tmpc_to_pix(data, pres)
        y = self.pres_to_pix(pres)
        for i in range(x.shape[0]-1):
            if y[i+1] > self.tpad:
                qp.drawLine(x[i], y[i], x[i+1], y[i+1])
            else:
                qp.drawLine(x[i], y[i], x[i+1], self.tpad+2)
                break
        label = (1.8 * data[0]) + 32.
        pen = QtGui.QPen(QtGui.QColor('#000000'), 0, QtCore.Qt.SolidLine)
        brush = QtGui.QBrush(QtCore.Qt.SolidPattern)
        qp.setPen(pen)
        qp.setBrush(brush)
        rect = QtCore.QRectF(x[0]-8, y[0]+4, 16, 12)
        qp.drawRect(rect)
        pen = QtGui.QPen(QtGui.QColor(color), 3, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.setFont(self.environment_trace_font)
        qp.drawText(rect, QtCore.Qt.AlignCenter, str(int(label)))
