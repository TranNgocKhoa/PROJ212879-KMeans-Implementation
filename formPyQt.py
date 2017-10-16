import sys
from PyQt4.QtGui import *
import mymain

class Form(QMainWindow):
    def __init__(self):
        super(Form, self).__init__()
        screenSize = QDesktopWidget().screenGeometry()
        width, height = screenSize.width(), screenSize.height()
        self.setGeometry(width/2-300, height/2-250, 600, 500)
        self.setWindowTitle("K-Mean Clustering")
        self.setWindowIcon(QIcon("pycharm.png"))
        self.setCentralWidget(ControlWidget())

        self.show()


class ControlWidget(QWidget):
    def __init__(self):
        super(ControlWidget, self).__init__()
        self.fname = "out.txt"
        self.formLayout = QFormLayout()
        self.buttonRun = QPushButton("RUN")
        self.buttonBrowse = QPushButton("File Select")
        self.labelFName = QLabel()
        self.labelFName.resize(550, 15)
        self.txtK = QLineEdit()
        self.txtK.setValidator(QIntValidator())
        self.txtK.setText('5')
        self.statusBox = StatusWidget()
        self.formLayout.addWidget(self.buttonBrowse)
        self.formLayout.addWidget(self.labelFName)
        self.formLayout.addWidget(self.buttonRun)
        self.formLayout.addWidget(self.statusBox)
        self.formLayout.addRow("Number of K:", self.txtK)
        self.buttonBrowse.clicked.connect(self.getfile)
        self.buttonRun.clicked.connect(self.run_kmean)
        self.setLayout(self.formLayout)


    def getfile(self):
        self.fname = QFileDialog.getOpenFileName(self, 'Open file', '', "*")
        self.labelFName.setText(self.fname)

    def run_kmean(self):
        numOfK = int(self.txtK.text())
        print numOfK
        gX = mymain.input_data(self.fname)
        print self.fname
        #(gcenters, glabels, git) = mymain.kmeans(gX, 5)
        (gcenters, glabels, git) = mymain.loop_100_kmeans(gX, 5)
        stringOut =  'Center of each clusters found by algorithm:\n'
        for i in range (len(gcenters)):
            stringOut += str(gcenters[i]) + "\n"
            self.statusBox.textBox.setPlainText(stringOut)



class StatusWidget(QWidget):
    def __init__(self):
        super(StatusWidget, self).__init__()
        boxLayout = QBoxLayout(QBoxLayout.Down)
        self.textBox = QPlainTextEdit()
        self.textBox.resize(600, 300)
        boxLayout.addWidget(self.textBox)
        self.setLayout(boxLayout)




app = QApplication(sys.argv)
GUI = Form()
sys.exit(app.exec_())
