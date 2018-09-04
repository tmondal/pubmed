import sys
from PyQt5.QtWidgets import (QWidget,QVBoxLayout,QPushButton,QScrollArea,QFormLayout,QLabel,QApplication,QMainWindow)

from PyQt5.QtCore import *

# from pyqt import App

class MoreMeshTerms(object):
    
    def setupUi(self,duplicate,parent, mesh_terms, mesh_terms_id):
        self.mesh_terms = mesh_terms
        self.mesh_terms_id = mesh_terms_id
        self.duplicate = duplicate
        self.centralWidget = QWidget(parent)
        # main layout
        self.vLayout = QVBoxLayout(self.centralWidget)
        parent.resize(600,600)

        # main button
        # self.pButton_add = QPushButton(self.centralWidget)
        # self.pButton_add.setText('Show all mesh terms')

        # scroll area
        self.scrollArea = QScrollArea(self.centralWidget)
        self.scrollArea.setWidgetResizable(True)

        # scroll area widget contents
        self.scrollAreaWidgetContents = QWidget(self.scrollArea)

        # scroll area widget contents - layout
        self.formLayout = QFormLayout(self.scrollAreaWidgetContents)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        # add all main to the main vLayout
        # self.vLayout.addWidget(self.pButton_add)
        self.vLayout.addWidget(self.scrollArea)
        # set central widget
        parent.setCentralWidget(self.centralWidget)
        # connections
        # self.pButton_add.clicked.connect(self.addbutton)


    # def addbutton(self):
        i = 1
        for x in range(0,len(self.mesh_terms)):
            cl = ClusterLabel(self.scrollAreaWidgetContents,i)
            i = i + 1
            count = self.formLayout.rowCount()
            self.formLayout.setWidget(count, QFormLayout.LabelRole, cl)
            for y in range(0,len(self.mesh_terms[x])):
                z = TermButton(self.scrollAreaWidgetContents,self.mesh_terms[x][y],self.mesh_terms_id[x][y],self.duplicate)
                c1 = self.formLayout.rowCount()
                self.formLayout.setWidget(c1, QFormLayout.LabelRole, z)

               
    # def getTermId(self):
    #     pass

class ClusterLabel(QLabel):
    def __init__(self,parent,data):
        super(ClusterLabel, self).__init__()
        self.setText("Cluster " + str(data) + " :")

class TermButton(QPushButton):
    def __init__(self,parent,term,_id,duplicate):
        self.duplicate = duplicate
        self.id = _id
        super(TermButton, self).__init__()
        self.setText(term)
        self.clicked.connect(self.term_clicked)

    def term_clicked(self):
        print("Hello")
        self.duplicate.populateTitleAbs(self.id)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    ex = MoreMeshTerms()
    ex.setupUi(window,None,None)
    window.show()
    sys.exit(app.exec_())