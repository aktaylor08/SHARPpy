import sys
import numpy as np
from PySide import QtGui, QtCore
from sharppy.viz import plotSkewT, plotHodo

from sounding import prof


# Setup Application
app = QtGui.QApplication(sys.argv)
mainWindow = QtGui.QMainWindow()
mainWindow.setGeometry(50, 50, 1000, 800)
title = 'SHARPpy: Sounding and Hodograph Analysis and Research Program '
title += 'in Python'
mainWindow.setWindowTitle(title)
mainWindow.setStyleSheet("QMainWindow {background-color: rgb(0, 0, 0);}")
centralWidget = QtGui.QFrame()
mainWindow.setCentralWidget(centralWidget)
grid = QtGui.QGridLayout()
grid.setHorizontalSpacing(0)
grid.setVerticalSpacing(2)
centralWidget.setLayout(grid)

# Handle the Upper Left
sound = plotSkewT(prof.pres, prof.hght, prof.tmpc, prof.dwpc)
sound.setContentsMargins(0, 0, 0, 0)
grid.addWidget(sound, 0, 0, 3, 1)

# Handle the Upper Right
urparent = QtGui.QFrame()
urparent_grid = QtGui.QGridLayout()
urparent_grid.setContentsMargins(0, sound.tpad-1, 0, sound.bpad-1)
urparent.setLayout(urparent_grid)
ur = QtGui.QFrame()
ur.setStyleSheet("QFrame {"
                 "  background-color: rgb(0, 0, 0);"
                 "  border-width: 1px;"
                 "  border-style: solid;"
                 "  border-color: rgb(255, 255, 255);"
                 "  margin: 0px;}")
grid2 = QtGui.QGridLayout()
grid2.setHorizontalSpacing(0)
grid2.setVerticalSpacing(0)
grid2.setContentsMargins(0, 0, 0, 0)
ur.setLayout(grid2)
speed_vs_height = QtGui.QFrame()
speed_vs_height.setObjectName("svh")
inferred_temp_advection = QtGui.QFrame()
hodo = plotHodo(prof.hght, prof.u, prof.v)
storm_slinky = QtGui.QFrame()
thetae_vs_pressure = QtGui.QFrame()
srwinds_vs_height = QtGui.QFrame()
watch_type = QtGui.QFrame()
grid2.addWidget(speed_vs_height, 0, 0, 10, 3)
grid2.addWidget(inferred_temp_advection, 0, 3, 10, 2)
grid2.addWidget(hodo, 0, 5, 8, 24)
grid2.addWidget(storm_slinky, 8, 5, 2, 6)
grid2.addWidget(thetae_vs_pressure, 8, 11, 2, 6)
grid2.addWidget(srwinds_vs_height, 8, 17, 2, 6)
grid2.addWidget(watch_type, 8, 23, 2, 6)
urparent_grid.addWidget(ur)
grid.addWidget(urparent, 0, 1, 3, 1)

# Handle the Text Areas
text = QtGui.QFrame()
text.setStyleSheet("QFrame {"
                   "  background-color: rgb(0, 0, 0);"
                   "  border-width: 2px;"
                   "  border-style: solid;"
                   "  border-color: #3399CC;}")
grid3 = QtGui.QGridLayout()
grid3.setHorizontalSpacing(0)
thermo = QtGui.QFrame()
grid3.setContentsMargins(0, 0, 0, 0)
kinematic = QtGui.QFrame()
misc1 = QtGui.QFrame()
misc2 = QtGui.QFrame()
grid3.addWidget(thermo, 0, 0)
grid3.addWidget(kinematic, 0, 1)
grid3.addWidget(misc1, 0, 2)
grid3.addWidget(misc2, 0, 3)
text.setLayout(grid3)
grid.addWidget(text, 3, 0, 1, 2)
mainWindow.show()
app.exec_()
