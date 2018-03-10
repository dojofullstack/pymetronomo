import sys
from time import sleep
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5.uic import loadUi
from PyQt5.QtMultimedia import QSound



__autor__ = 'Henry Vasquez Conde'


class App(QMainWindow):
    def __init__(self, *args):
        super(App, self).__init__(*args)
        loadUi('interface.ui', self)
        with open('style.css') as f:
            style = f.read()
        self.setStyleSheet(style) 
        self.conexiones()

    def conexiones(self):
        self.pushButton_8.clicked.connect(self.moderato)
        self.pushButton_5.clicked.connect(self.allegretto)
        self.pushButton_6.clicked.connect(self.allegro)
        self.pushButton_7.clicked.connect(self.vivace)
        self.pushButton_1.clicked.connect(self.presto)
        self.pushButton_2.clicked.connect(self.prestissimo)
        self.pushButton_3.clicked.connect(self.pause)
        self.pushButton_4.clicked.connect(self.metronomo)
        self.values()

    def values(self):
        self.ani1 = self.ani2 = self.ani3 = True
        self.bpm = 90
        self.spinBox.setValue(self.bpm)

    def moderato(self):
        self.bpm = 70
        self.spinBox.setValue(self.bpm)

    def allegretto(self):
        self.bpm = 96
        self.spinBox.setValue(self.bpm)

    def allegro(self):
        self.bpm = 113
        self.spinBox.setValue(self.bpm)

    def vivace(self):
        self.bpm = 121
        self.spinBox.setValue(self.bpm)

    def presto(self):
        self.bpm = 141
        self.spinBox.setValue(self.bpm)

    def prestissimo(self):
        self.bpm = 176
        self.spinBox.setValue(self.bpm)

    def play_wav(self):
        self.tono = QSound('./default.wav')
        self.tono.play()
        self.animation()

    def metronomo(self):
        self.bpm = self.spinBox.value()
        self.thread = PyMetronomoThread(self.bpm)
        self.thread.signals.play.connect(self.play_wav)
        self.thread.start()
        self.pushButton_4.setVisible(False)
        self.pushButton_3.setVisible(True)

    def pause(self):
        self.ani1 = self.ani2 = self.ani3 = True
        self.animation3.setStyleSheet('background: #288a66; border-radius: 16px;')
        self.animation1.setStyleSheet('background: #288a66; border-radius: 16px;')
        self.animation2.setStyleSheet('background: #288a66; border-radius: 16px;')
        self.pushButton_4.setVisible(True)
        self.pushButton_3.setVisible(False)
        self.thread.stop()

    def animation(self):
        if self.ani1:
            # self.reset()
            self.animation1.setStyleSheet('background: #34d96e; border-radius: 20px;')
            self.animation2.setStyleSheet('background: #288a66; border-radius: 16px;')
            self.animation3.setStyleSheet('background: #288a66; border-radius: 16px;')
            self.ani1 = False
        elif self.ani2:
            self.animation2.setStyleSheet('background: #34d96e; border-radius: 20px;')
            self.animation1.setStyleSheet('background: #288a66; border-radius: 16px;')
            self.animation3.setStyleSheet('background: #288a66; border-radius: 16px;')
            self.ani2 = False
        elif self.ani3:
            self.animation3.setStyleSheet('background: #34d96e; border-radius: 20px;')
            self.animation1.setStyleSheet('background: #288a66; border-radius: 16px;')
            self.animation2.setStyleSheet('background: #288a66; border-radius: 16px;')
            self.ani1 = self.ani2 = self.ani3 = True

    def reset(self):
        self.animation3.setStyleSheet('background: #288a66; border-radius: 16px;')
        self.animation1.setStyleSheet('background: #288a66; border-radius: 16px;')
        self.animation2.setStyleSheet('background: #288a66; border-radius: 16px;')

class PyMetronomoThread(QThread):
    def __init__(self, bpm, parent=None):
        super(PyMetronomoThread, self).__init__(parent)
        self.bpm = bpm
        self.active = True
        self.signals = Communicate()

    def stop(self):
        self.active = False

    def run(self):
        delay = 60/self.bpm
        while self.active:
            self.signals.play.emit()
            sleep(delay)

class Communicate(QObject):
    play = pyqtSignal()


app = QApplication(sys.argv)

widget = App()
widget.show()
sys.exit(app.exec_())