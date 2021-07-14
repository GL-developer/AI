import time, sys
from PyQt5 import uic,QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from imageAI.imageAI import *
from dobot import dobot
form = uic.loadUiType("image.ui")[0]
zero = False
class Thread(QThread):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent = parent
        self.recoding=True
        
    def run(self):
        global zero
        dobot.init()
        while self.recoding:
            self.image = getImageResource(224,224)
            data = getAnalyzedData(self.image, self.parent.model)
            labels = getTextLabel('imageAI/labels.txt')
            self.image = QtGui.QImage(self.image.data, self.image.shape[1],self.image.shape[0], QtGui.QImage.Format_RGB888).rgbSwapped()
            self.parent.imageLabel.setPixmap(QtGui.QPixmap.fromImage(self.image))
            text= ""
            max_index = 0
            for index, value in enumerate(data):
                text += labels[index]+": "+str(np.around(value*100,2))+"%\n"
                if data[max_index] < value:
                    max_index = index
            self.parent.classLabel.setText(text)
            if max_index == 0:
                zero = True
            elif zero:
                if max_index == 1:
                    From = {'X':200, 'Y':100, 'Z':-40, 'R':0}
                    To = {'X':200, 'Y':-100, 'Z':-40, 'R':0}
                    height = 0
                    dobot.PickAndPlace(From,To,height)
                    zero = False
                elif max_index == 2:
                    From = {'X':200, 'Y':-100, 'Z':-40, 'R':0}
                    To = {'X':200, 'Y':100, 'Z':-40, 'R':0}
                    height = 0
                    dobot.PickAndPlace(From,To,height)
                    zero = False
                    
class WindowClass(QMainWindow, form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.th = Thread(self)
        self.model = loadModel('imageAI/keras_model.h5')
        self.startButton.clicked.connect(self.actionStart)
        self.stopButton.clicked.connect(self.actionStop)

    def actionStart(self):
        self.th.recoding=True
        self.th.start()
    
    def actionStop(self):
        self.th.recoding = False
        dobot.disconnect()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = WindowClass()
    MainWindow.show()
    sys.exit(app.exec_())

