# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'twomenu.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import matplotlib
import matplotlib.pyplot as plt

from userInterface import MatplotlibCanvas

matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as Navi
from matplotlib.figure import Figure
import seaborn as sns
import pandas as pd
import sip

from PyQt5 import QtCore, QtGui, QtWidgets


class secondWindow(object):
    def setupUi(self, secondWindow):
        secondWindow.setObjectName("MainWindow")
        secondWindow.resize(802, 607)
        self.centralwidget = QtWidgets.QWidget(secondWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 0, 401, 24))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.pushButton_3 = QtWidgets.QPushButton(self.widget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.widget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout.addWidget(self.pushButton_4)
        secondWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(secondWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 802, 18))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        secondWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(secondWindow)
        self.statusbar.setObjectName("statusbar")
        secondWindow.setStatusBar(self.statusbar)
        self.actionOpen_CSV_File = QtWidgets.QAction(secondWindow)
        self.actionOpen_CSV_File.setObjectName("actionOpen_CSV_File")
        self.actionExit = QtWidgets.QAction(secondWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuFile.addAction(self.actionOpen_CSV_File)
        self.menuFile.addAction(self.actionExit)
        self.menubar.addAction(self.menuFile.menuAction())

       # self.pushButton.clicked.connect(self.getFile)
       # self.pushButton_2.clicked.connect(self.getFile)
       # self.pushButton_3.clicked.connect(self.getFile)
       # self.pushButton_4.clicked.connect(self.getFile)


        self.retranslateUi(secondWindow)
        QtCore.QMetaObject.connectSlotsByName(secondWindow)

        self.filename = ''
        self.canv = MatplotlibCanvas(self)
        self.df = []

        self.toolbar = Navi(self.canv, self.centralwidget)
        self.horizontalLayout.addWidget(self.toolbar)

    def getFile(self):
        """ This function will get the address of the csv file location
            also calls a readData function
        """
        self.filename = QFileDialog.getOpenFileName(filter="csv (*.csv)")[0]
        print("File :", self.filename)
        self.readData()

    def readData(self):
        """ This function will read the data using pandas and call the update
            function to plot
        """
        import os
        base_name = os.path.basename(self.filename)
        self.Title = os.path.splitext(base_name)[0]
        print('FILE', self.Title)
        self.df = pd.read_csv(self.filename, encoding='utf-8').fillna(0)
        self.Update(self.themes[0])  # lets 0th theme be the default : bmh

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Menu: "))

        self.pushButton.setText(_translate("MainWindow", "Popular Movies Ranking"))
        self.pushButton_2.setText(_translate("MainWindow", "Popular Shows Ranking"))
        self.pushButton_3.setText(_translate("MainWindow", "Top 250 Movies"))
        self.pushButton_4.setText(_translate("MainWindow", "Top 250 Shows"))

        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionOpen_CSV_File.setText(_translate("MainWindow", "Open CSV File"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = secondWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
