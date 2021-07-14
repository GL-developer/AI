import time, sys
from PyQt5 import uic,QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from voiceAI import record, stt, tts, transfer
from voiceAI.common import *
from dobot import dobot
import vlc

acronym = ['kr','en','jp','cn','vi','id','ar','bn','de','es','fr']

form = uic.loadUiType("voice.ui")[0]

class WindowClass(QMainWindow, form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.recordButton.clicked.connect(self.startRecord)
        self.stopButton.clicked.connect(self.stopRecord)
        self.STTRadio.clicked.connect(self.changeRadio)
        self.TransferRadio.clicked.connect(self.changeRadio)
        self.TTSSendButton.clicked.connect(self.sendTTS)
        self.toCombobox.addItems(acronym)
        self.toLabel.setVisible(False)
        self.toCombobox.setVisible(False)
        
    def changeRadio(self):
        if self.STTRadio.isChecked():
            self.toLabel.setVisible(False)
            self.toCombobox.setVisible(False)
            
        elif self.TransferRadio.isChecked():
            self.toLabel.setVisible(True)
            self.toCombobox.setVisible(True)
            
    def startRecord(self):
        record.start()
        
    def stopRecord(self):
        record.stop()
        res = stt.getSTT()
        if self.STTRadio.isChecked():
            self.resultLabel.setText(res)
        elif self.TransferRadio.isChecked():
            from_lang = transfer.senseSpeech(latin2utf8(res))
            to_lang = self.toCombobox.currentText()
            res = transfer.transLang(from_lang,to_lang,res)
            self.resultLabel.setText(res)
            tts.getTTS(latin2utf8(res))
            vlc.MediaPlayer(getWavPath()).play()
        print(res)
        if res == "하나" or res =="1":
            From = {'X':200, 'Y':100, 'Z':-40, 'R':0}
            To = {'X':200, 'Y':-100, 'Z':-40, 'R':0}
            height = 0
            dobot.PickAndPlace(From,To,height)
        elif res == "둘" or res =="2":
            From = {'X':200, 'Y':-100, 'Z':-40, 'R':0}
            To = {'X':200, 'Y':100, 'Z':-40, 'R':0}
            height = 0
            dobot.PickAndPlace(From,To,height)
    def sendTTS(self):
        tts.getTTS(latin2utf8(self.TTSText.toPlainText()))
        vlc.MediaPlayer(getWavPath()).play()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = WindowClass()
    MainWindow.show()
    dobot.init()
    sys.exit(app.exec_())