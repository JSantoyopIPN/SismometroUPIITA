from datetime import datetime
import PyQt5
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTabWidget, QMenuBar, QStatusBar, QGridLayout, QMessageBox
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib, matplotlib.cm as cm
import sys, os, serial, time, csv
from numpy import arange, sin, pi, random, linspace
from math import pi
import numpy as np

import threading
from threading import Thread

serData = serial.Serial(
    port = 'COM3',
    baudrate = 115200,
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE,
    bytesize = serial.EIGHTBITS,
    timeout = None
    #timeout = 1
)

# headerCSV = ['Fecha', 'Amplitud']
# dataCSV = []
# fileNameCSV = 'Datos_CSV_' + str(datetime.now())
# fileNameCSV = fileNameCSV.replace(":","-")

# with open(fileNameCSV, 'w', encoding='UTF8', newline='') as f:
#             writer = csv.writer(f)
#             writer.writerow(headerCSV)

class SignalCommunicate(PyQt5.QtCore.QObject):
    LehmanFFTUpdate = PyQt5.QtCore.pyqtSignal()
    LaCosteFFTUpdate = PyQt5.QtCore.pyqtSignal()

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, signalUpdateInterval = 15):        
        super(Ui_MainWindow, self).__init__()
        uic.loadUi("GUI_Sismografo_C.ui", self) # Cargar interfaz (ui) 
        self.show() # Muestra interfaz
        
        self.samplesOnScreen = 2000 # Número de muestras que se mostrarán en pantalla
        self.xLehman = list(range(self.samplesOnScreen))
        self.yLehman = list(list([1.6] * self.samplesOnScreen))
        self.xLaCoste = list(range(self.samplesOnScreen))
        self.yLaCoste = list(list([1.6] * self.samplesOnScreen))
        self.hex_ser = ['0x00','0x00']
        self.hex_val = 0 
        
        self.xLehmanFFT = list(range(10))
        self.yLehmanFFT = list(list([10] * 10))
        
        pen = pg.mkPen(color = (27, 103, 107))
        self.dataLineLehman =  self.graphViewLehmanSignal.plot(self.xLehman, self.yLehman, pen = pen)   
        self.graphViewLehmanSignal.setBackground('w')
        self.graphViewLehmanSignal.setLogMode(x = False, y = False)
        self.graphViewLehmanSignal.showGrid(x = True, y = True)
        self.graphViewLehmanSignal.setLabel('left', "Amplitud (V)")
        self.graphViewLehmanSignal.setLabel('bottom', "Tiempo (HH:MM:SS)")
        #self.graphViewLehmanSignal.setYRange(1, 3)
        
        self.dataLineLehmanFourier = self.graphViewLehmanFourier.plot(self.xLehmanFFT, self.yLehmanFFT, pen = pen)
        self.graphViewLehmanFourier.setBackground('w')
        self.graphViewLehmanFourier.setLogMode(x = False, y = False)
        self.graphViewLehmanFourier.showGrid(x = True, y = True)
        self.graphViewLehmanFourier.setLabel('left', "Amplitud (V)")
        self.graphViewLehmanFourier.setLabel('bottom', "Rango de frecuencias (Hz)")
        #self.graphViewLaCosteFourier.setYRange(1, 3)
        
        self.dataLineLaCoste =  self.graphViewLaCosteSignal.plot(self.xLehman, self.yLehman, pen = pen)   
        self.graphViewLaCosteSignal.setBackground('w')
        self.graphViewLaCosteSignal.setLogMode(x = False, y = False)
        self.graphViewLaCosteSignal.showGrid(x = True, y = True)
        self.graphViewLaCosteSignal.setLabel('left', "Amplitud (V)")
        self.graphViewLaCosteSignal.setLabel('bottom', "Tiempo (HH:MM:SS)")
        #self.graphViewLaCosteSignal.setYRange(1, 3)    
        
        self.dataLineLaCosteFourier = self.graphViewLaCosteFourier.plot(self.xLehmanFFT, self.yLehmanFFT, pen = pen)
        self.graphViewLaCosteFourier.setBackground('w')
        self.graphViewLaCosteFourier.setLogMode(x = False, y = False)
        self.graphViewLaCosteFourier.showGrid(x = True, y = True)
        self.graphViewLaCosteFourier.setLabel('left', "Amplitud (V)")
        self.graphViewLaCosteFourier.setLabel('bottom', "Rango de frecuencias (Hz)")
        #self.graphViewLaCosteFourier.setYRange(1, 3)
        
        self.timer = QtCore.QTimer()
        # self.freq_plot = []
        # self.ts_plot = []
        
        #self.timer.setInterval(15)
        self.timer.timeout.connect(self.updateSignalPlot)
        self.timer.timeout.connect(self.updateFourierPlot)
        self.timer.start()
            
    def readSignals(self):
        self.serialDataASCII = serData.readline() # Lectura de datos desde Arduino (ASCII)
        self.xLehman = self.xLehman[1:]  # Elimina el primer elemento en y.
        self.xLehman.append(self.xLehman[-1] + 1)  # Añade un nuevo elemento más grande que el previo.
        self.yLehman = self.yLehman[1:]  # Elimina en el primer elemento de la lista.
        
        self.xLaCoste = self.xLaCoste[1:]  # Elimina el primer elemento en y.   
        self.xLaCoste.append(self.xLaCoste[-1] + 1)  # Añade un nuevo elemento más grande que el previo.
        self.yLaCoste = self.yLaCoste[1:]  # Elimina en el primer elemento de la lista.
        
        stringData = str(self.serialDataASCII.decode('cp437'))
        stringData = stringData.replace("\n","")
        stringData = stringData.replace("\r","")
        listData = stringData.split(" ")

        LehmanData = listData[1][1:] 
        LaCosteData = listData[0][1:]     
        self.voltageLehman = (int(LehmanData) * 6.144) / 32768
        self.voltageLaCoste = (int(LaCosteData) * 6.144) / 32768
        
    def updateSignalPlot(self): 
        self.readSignals()
        
        # with open(fileNameCSV, 'a', encoding='UTF8', newline='') as f:
        #     writer = csv.writer(f)
        #     writer.writerow([str(datetime.now()), str(self.serialDataASCII)])      
        
        self.yLehman.append(self.voltageLehman)
        self.dataLineLehman.setData(self.xLehman, self.yLehman)  # Actualiza
        self.yLaCoste.append(self.voltageLaCoste)
        self.dataLineLaCoste.setData(self.xLaCoste, self.yLaCoste)  # Actualiza
            
    def updateFourierPlot(self): 
        if self.xLehman[-1] >= (self.samplesOnScreen*2):
            dt = 0.015
            FFTLehman = self.FFTParams(self.yLehman, dt)
            self.dataLineLehmanFourier.setData(FFTLehman[0], np.abs(FFTLehman[1]))
            FFTLaCoste = self.FFTParams(self.yLaCoste, dt)
            self.dataLineLaCosteFourier.setData(FFTLaCoste[0], np.abs(FFTLaCoste[1]))
        
    def FFTParams(self,TimeSeries,dt):
        """"
        TimeSeries: Serie de tiempo
        t0 = tiempo inicial de la serie (debería empezar en cero)
        dt: Tiempo de muestro (s) (o longitud temporal entre dos muestras)
        Fs: Frecuencia de muestreo
        freqTs: Frecuencia FFT considerando TMA Nyquist
        fftHalfTS: FFT considerando TMA Nyquist 
        """
        Fs = 1/dt
        Ns=len(TimeSeries) #Número total de datos de la serie de tiempo
        #Valor promedio de la señal muestreada
        tSMean = np.mean(TimeSeries)
        #Señal muestreada convertida a AC y normalizada
        tSAC =  TimeSeries - tSMean
        tSMax= np.max(tSAC)
        tSACNorm =tSAC/tSMax
        #Transformada de Fourier de la serie de tiempo
        fftTS =np.fft.fft(tSACNorm)
        #Mitad de los puntos de la serie original
        halfPoints=int(len(TimeSeries) /2)
        freqTs = []
        for i in range(0,halfPoints):
            freqTs.append((i*Fs)/Ns)
        fftHalfTS=[]
        for i in range(0, len(freqTs)):
            fftHalfTS.append(fftTS[i])
        #Dado que se pierden la mitad de los puntos originales a consecuencia
        #del teorema de Nyquist, se crea un nuevo vector de tiempo para reconstruir
        #la señal
        recTime = []

        for i in range(0,halfPoints):
            recTime.append((2*i)*dt)
        #Reconstrucción  de la serie muestreada acondicionada
        #con la mitad la serie de la FFT 
        recSerie = np.fft.ifft(fftHalfTS)

        #Reconstrucción con la amplitud y el promedio de la serie 
        #muestreada original
        recSerie *= tSMax
        recSerie += tSMean
        return [freqTs,fftHalfTS,recTime,recSerie]
    
    def closeEvent(self, event):
        super(Ui_MainWindow, self).closeEvent(event)
        try:
            self.timer.stop()
            serData.close()
        except:
            QMessageBox.critical(self, 'Excepción en Puerto Serial', 'Hubo un fallo al cerrar el puerto serial.\n Por favor, ¡reinicie la aplicación!')
            return None

# Inicialización de GUI
def main():
    if not QtWidgets.QApplication.instance():
        QtWidgets.QApplication(sys.argv)
    else:
        QtWidgets.QApplication.instance()
    main = Ui_MainWindow()
    main.show()

    return main

if __name__ == '__main__':         
    m = main()