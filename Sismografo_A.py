import PyQt5
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTabWidget, QMenuBar, QStatusBar, QGridLayout
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
import threading
from threading import Thread
from datetime import datetime
import numpy as np
import sys, os, serial, time, csv

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
    LehmanData = PyQt5.QtCore.pyqtSignal(float)
    LaCosteData = PyQt5.QtCore.pyqtSignal(float)

    LehmanDataUpdate = PyQt5.QtCore.pyqtSignal()
    LehmanFFTUpdate = PyQt5.QtCore.pyqtSignal()
    LaCosteDataUpdate = PyQt5.QtCore.pyqtSignal()
    LaCosteFFTUpdate = PyQt5.QtCore.pyqtSignal()

class Ui_MainWindow(QtWidgets.QMainWindow):   
    def __init__(self):        
        super(Ui_MainWindow, self).__init__()
        uic.loadUi("GUI_Sismografo_A.ui", self) # Cargar interfaz (ui) 
        self.show() # Muestra interfaz
        
        self.xLehman = list(range(2000))
        self.yLehman = list(list([1.6] * 2000))
        self.xLaCoste = list(range(2000))
        self.yLaCoste = list(list([1.6] * 2000))
        self.hex_ser = ['0x00','0x00']
        self.hex_val = 0 
        
        self.xLehmanFFT = list(range(10))
        self.yLehmanFFT = list(range(10))
        
        pen = pg.mkPen(color = (27, 103, 107))
        self.dataLineLehman =  self.graphViewLehmanSignal.plot(self.xLehman, self.yLehman, pen = pen)   
        self.graphViewLehmanSignal.setBackground('w')
        self.graphViewLehmanSignal.setLogMode(x = False, y = False)
        self.graphViewLehmanSignal.showGrid(x = True, y = True)
        self.graphViewLehmanSignal.setLabel('left', "Amplitud (V)")
        self.graphViewLehmanSignal.setLabel('bottom', "Tiempo (HH:MM:SS)")
        #self.graphViewLehmanSignal.setYRange(1, 3)
        
        self.dataLineLaCosteFourier = self.graphViewLaCosteFourier.plot(self.xLehmanFFT, self.yLehmanFFT, pen = pen)
        self.graphViewLaCosteFourier.setBackground('w')
        self.graphViewLaCosteFourier.setLogMode(x = False, y = False)
        self.graphViewLaCosteFourier.showGrid(x = True, y = True)
        self.graphViewLaCosteFourier.setLabel('left', "Amplitud (V)")
        self.graphViewLaCosteFourier.setLabel('bottom', "Rango de frecuencias (Hz)")
        #self.graphViewLaCosteFourier.setYRange(1, 3)
        
        self.dataLineLaCoste =  self.graphViewLaCosteSignal.plot(self.xLehman, self.yLehman, pen = pen)   
        self.graphViewLaCosteSignal.setBackground('w')
        self.graphViewLaCosteSignal.setLogMode(x = False, y = False)
        self.graphViewLaCosteSignal.showGrid(x = True, y = True)
        self.graphViewLaCosteSignal.setLabel('left', "Amplitud (V)")
        self.graphViewLaCosteSignal.setLabel('bottom', "Tiempo (HH:MM:SS)")
        #self.graphViewLaCosteSignal.setYRange(1, 3)      
                        
        self.timer = QtCore.QTimer()
        self.freq_plot = []
        self.ts_plot = []
        #self.timer.setInterval(5)
        self.timer.timeout.connect(self.updateSignalPlot)
        self.timer.start()
    
    def updateSignalPlot(self): 
        data = serData.readline() # Lectura de datos desde Arduino (ASCII)
        # with open(fileNameCSV, 'a', encoding='UTF8', newline='') as f:
        #     writer = csv.writer(f)
        #     writer.writerow([str(datetime.now()), str(data)])
        
        self.xLehman = self.xLehman[1:]  # Elimina el primer elemento en y.
        #timeData = datetime.now()
        #self.x.append(time.strftime("%H:%M:%S"))     
        self.xLehman.append(self.xLehman[-1] + 1)  # Añade un nuevo elemento más grande que el previo.
        self.yLehman = self.yLehman[1:]  # Elimina en el primer elemento de la lista.
        
        self.xLaCoste = self.xLaCoste[1:]  # Elimina el primer elemento en y.   
        self.xLaCoste.append(self.xLaCoste[-1] + 1)  # Añade un nuevo elemento más grande que el previo.
        self.yLaCoste = self.yLaCoste[1:]  # Elimina en el primer elemento de la lista.
        
        stringData = str(data.decode('cp437'))
        stringData = stringData.replace("\n","")
        stringData = stringData.replace("\r","")
        listData = stringData.split(" ")
        
        # if listData[0][0] == 'A':
        #     LehmanData = listData[0][1:] 
        #     LaCosteData = listData[1][1:]
        # elif listData[0][0] == 'B':
        #     LehmanData = listData[1][1:]
        #     LaCosteData = listData[0][1:]
        
        LehmanData = listData[0][1:] 
        LaCosteData = listData[1][1:]     
        voltageLehman = (int(LehmanData) * 6.144) / 32768
        voltageLaCoste = (int(LaCosteData) * 6.144) / 32768
        
        self.yLehman.append(voltageLehman)
        self.dataLineLehman.setData(self.xLehman, self.yLehman)  # Actualiza
        self.yLaCoste.append(voltageLaCoste)
        self.dataLineLaCoste.setData(self.xLaCoste, self.yLaCoste)  # Actualiza
        
        if self.xLehman[-1] >= 8000:
            dt = 0.015
            transformada = self.FFTParams(self.yLehman,dt)
            self.dataLineLaCosteFourier.setData(transformada[0], np.abs(transformada[1]))
            
        # dt = 0.015
        # transformada = self.FFTParams(self.yLehman,dt)
        # self.dataLineLaCosteFourier.setData(transformada[0], np.abs(transformada[1]))
            
            
        # if self.xLehman[-1] >= 4000:
        #     dt = 0.015
        #     transformada = self.FFTParams(self.yLehman[-1000:],dt)
        #     self.dataLineLaCosteFourier.setData(transformada[0], np.abs(transformada[1]))
        #     len(transformada)
        
        # if self.count == 200:
        #     dt = 0.015
        #     transformada = self.FFTParams(self.ts_plot,dt)
        #     self.dataLineLaCosteFourier.setData(transformada[0], np.abs(transformada[1]))
        #     self.ts_plot = []
        #     self.count = 0
        # self.ts_plot.append(voltageLaCoste)
        # self.count = self.count + 1
        
            # x=range(0, 10) 
            # y=range(0, 20, 2)
            # self.plotWidget.canvas.ax.plot(x, y)
            # self.plotWidget.canvas.draw()
            
            # self.canvas.axes.cla()
            # self.canvas.axes.set_ylabel("Voltage (V)")
            # self.canvas.axes.plot(transformada[0],np.abs(transformada[1]),'C1--')
            # self.canvas.draw()    
    
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
           

# Inicialización de GUI
app = QtWidgets.QApplication(sys.argv)
UIWindow = Ui_MainWindow()
sys.exit(app.exec_())