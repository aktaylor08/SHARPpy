import numpy as np
from PySide import QtGui, QtCore


__all__ = ['skewT', 'plotSkewT']

class skewT(QtGui.QFrame):
    def __init__(self):
        super(skewT, self).__init__()
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
        self.roffset = self.wid * (1/9.)
        self.barbx = self.brx + self.roffset / 2
        self.log_pmax = np.log(1050.); self.log_pmin = np.log(self.pmin)
        self.bltmpc = -50; self.brtmpc = 50; self.dt = 10
        self.xskew = 100 / 3.
        self.xrange = self.brtmpc - self.bltmpc
        self.yrange = np.tan(np.deg2rad(self.xskew)) * self.xrange
        self.label_font = QtGui.QFont('Helvetica', 11)
        self.environment_trace_font = QtGui.QFont('Helvetica', 11)

    def resizeEvent(self, e):
        '''
        Resize the plot based on adjusting the main window.

        '''
        self.initUI()

    def paint(self):
        qp = QtGui.QPainter()
        qp.begin(self)
        for t in range(self.bltmpc-100, self.brtmpc+self.dt+100, self.dt):
            self.draw_isotherm(t, qp)
        self.draw_frame(qp)
        for p in [1000, 850, 700, 500, 300, 200, 100]:
            self.draw_isobar(p, 1, qp)
        for t in range(self.bltmpc, self.brtmpc+self.dt, self.dt):
            self.draw_isotherm_labels(t, qp)
        for p in range(int(self.pmax), int(self.pmin-50), -50):
            self.draw_isobar(p, 0, qp)

        # qp.drawLine(self.barbx, self.tpad, self.barbx, self.bry)

        qp.end()

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
        qp.drawLine(self.lpad, self.tpad, self.brx+self.roffset, self.tpad)
        qp.drawLine(self.brx+self.roffset, self.tpad, self.brx+self.roffset,
                    self.bry)
        qp.drawLine(self.brx+self.roffset, self.bry, self.lpad, self.bry)
        qp.drawLine(self.lpad, self.bry, self.lpad, self.tpad)

    def draw_isotherm_labels(self, t, qp):
        '''
        Add Isotherm Labels.

        '''
        pen = QtGui.QPen(QtGui.QColor("FFFFFF"))
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
        offset = int((self.brx - self.lpad) * 0.01)
        if flag:
            qp.drawLine(self.lpad, y1, self.brx, y1)
            qp.drawText(0, y1-20, self.lpad-4, 40,
                        QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight,
                        str(int(p)))
        else:
            qp.drawLine(self.lpad, y1, self.lpad+offset, y1)
            qp.drawLine(self.brx+self.roffset-offset, y1,
                        self.brx+self.roffset, y1)

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
        return y


class plotSkewT(skewT):
    def __init__(self, pres, hght, tmpc, dwpc):
        super(plotSkewT, self).__init__()
        self.pres = pres; self.hght = hght
        self.tmpc = tmpc; self.dwpc = dwpc

    def paintEvent(self, e):
        '''
        Draw the background features of a Skew-T.

        '''
        super(plotSkewT, self).paint()
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawTrace(self.dwpc, QtGui.QColor("#00CC00"), qp)
        self.drawTrace(self.tmpc, QtGui.QColor("#CC0000"), qp)
        qp.end()

    def drawTrace(self, data, color, qp):
        '''
        Draw an environmental trace.

        '''
        pen = QtGui.QPen(QtGui.QColor(color), 3, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        x = self.tmpc_to_pix(data, self.pres)
        y = self.pres_to_pix(self.pres)
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
