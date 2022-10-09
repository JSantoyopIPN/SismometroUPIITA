# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Escritorio\Sismografo_A\GUI_Sismografo_A.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 717)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 1001, 651))
        self.tabWidget.setObjectName("tabWidget")
        self.Horizontal = QtWidgets.QWidget()
        self.Horizontal.setObjectName("Horizontal")
        self.graphViewLehmanSignal = PlotWidget(self.Horizontal)
        self.graphViewLehmanSignal.setGeometry(QtCore.QRect(10, 10, 981, 291))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphViewLehmanSignal.sizePolicy().hasHeightForWidth())
        self.graphViewLehmanSignal.setSizePolicy(sizePolicy)
        self.graphViewLehmanSignal.setResizeAnchor(QtWidgets.QGraphicsView.AnchorViewCenter)
        self.graphViewLehmanSignal.setObjectName("graphViewLehmanSignal")
        self.widget = QtWidgets.QWidget(self.Horizontal)
        self.widget.setGeometry(QtCore.QRect(10, 320, 981, 291))
        self.widget.setObjectName("widget")
        self.graphViewLehmanFourier = PlotWidget(self.widget)
        self.graphViewLehmanFourier.setGeometry(QtCore.QRect(0, 0, 981, 291))
        self.graphViewLehmanFourier.setObjectName("graphViewLehmanFourier")
        self.tabWidget.addTab(self.Horizontal, "")
        self.Vertical = QtWidgets.QWidget()
        self.Vertical.setObjectName("Vertical")
        self.graphViewLaCosteSignal = PlotWidget(self.Vertical)
        self.graphViewLaCosteSignal.setGeometry(QtCore.QRect(10, 10, 981, 291))
        self.graphViewLaCosteSignal.setObjectName("graphViewLaCosteSignal")
        self.graphViewLaCosteFourier = PlotWidget(self.Vertical)
        self.graphViewLaCosteFourier.setGeometry(QtCore.QRect(10, 320, 981, 291))
        self.graphViewLaCosteFourier.setObjectName("graphViewLaCosteFourier")
        self.tabWidget.addTab(self.Vertical, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 21))
        self.menubar.setObjectName("menubar")
        self.menuArchivo = QtWidgets.QMenu(self.menubar)
        self.menuArchivo.setObjectName("menuArchivo")
        self.menuEditar = QtWidgets.QMenu(self.menubar)
        self.menuEditar.setObjectName("menuEditar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuArchivo.menuAction())
        self.menubar.addAction(self.menuEditar.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Horizontal), _translate("MainWindow", "Sismógrafo horizontal (Lehman)"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Vertical), _translate("MainWindow", "Sismógrafo vertical (LaCoste)"))
        self.menuArchivo.setTitle(_translate("MainWindow", "Archivo"))
        self.menuEditar.setTitle(_translate("MainWindow", "Editar"))

