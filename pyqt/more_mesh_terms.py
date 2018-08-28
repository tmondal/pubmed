import sys
from PyQt5.QtWidgets import (QDialog,QLabel,QPushButton,QVBoxLayout,QFormLayout,
    QWidget,QScrollArea,QApplication)


class MoreMeshTerms(QDialog):
    def __init__(self,mesh_terms,parent=None):
        super(MoreMeshTerms, self).__init__(parent)
        print("called")
        # # scroll area widget contents - layout
        # self.scrollLayout = QFormLayout()

        # # scroll area widget contents
        # self.scrollWidget = QWidget()
        # self.scrollWidget.setLayout(self.scrollLayout)

        # # scroll area
        # self.scrollArea = QScrollArea()
        # self.scrollArea.setWidgetResizable(True)
        # self.scrollArea.setWidget(self.scrollWidget)

        # # main layout
        self.mainLayout = QVBoxLayout()
        self.b1 = QPushButton("Button1")
        self.mainLayout.addWidget(self.b1)
        self.setWindowTitle("Button demo")

        # # add all main to the main vLayout
        # self.mainLayout.addWidget(self.scrollArea)

        # # central widget
        # self.centralWidget = QWidget()
        # self.centralWidget.setLayout(self.mainLayout)

        # set central widget
        # self.setCentralWidget(self.centralWidget)

        # Loop through each mesh term and add a button
        # i = 1
        # for terms in mesh_terms:
        #     self.scrollLayout.addRow(ClusterLabel(i))
        #     for term in terms:
        #         self.scrollLayout.addRow(TermButton(term))
        
        # self.show()
               
#     def getTermId(self):
#         pass

# class ClusterLabel(QLabel):
#     def __init__(self,data):
#         super(ClusterLabel, self).__init__()
#         self.setText("Cluster " + str(data) + " :")

# class TermButton(QPushButton):
#     def __init__(self,term):
#         super(TermButton, self).__init__()
#         self.setText(term)
#         self.clicked.connect(self.term_clicked)

#     def term_clicked(self):
#         print("Hello")

def main(mesh_terms):
    app = QApplication(sys.argv)
    ex = MoreMeshTerms(mesh_terms)
    ex.show()
    # sys.exit(app.exec_())