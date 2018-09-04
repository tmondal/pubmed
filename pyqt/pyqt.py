import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLineEdit, QMessageBox, 
	QLabel, QTextEdit, QGridLayout, QRadioButton, QFileDialog, QMainWindow, QDialog)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

import api
from goldencorpus import GoldenCorpus
from mesh_explosion import DataForEachMeshTerm
from clusterer import Clusterer
from postprocessing import PostProcessing
from more_mesh_terms import MoreMeshTerms
# import more_mesh_terms
 
class App(QWidget):

	def __init__(self):
		super().__init__()
		self.title = 'PyQt5'
		self.fileselected = 0
		self.fileName = ""
		self.rel_docs = []
		self.mesh_terms = []
		self.initUI()

	def initUI(self):
		self.setWindowTitle(self.title)
		self.showMaximized()	

		# Create grid
		self.grid = QGridLayout()
		self.setLayout(self.grid)
		self.grid.setSpacing(0)
		
		# Search field
		self.searchbox = QLineEdit(self)
		self.searchbox.setText('breast cancer')
		self.searchbox.move(50, 20)
		self.searchbox.resize(280,40)
		
		# Search button
		self.button = QPushButton('Search', self)
		self.button.setToolTip('Search')
		self.button.clicked.connect(self.search_click)

		# Add first row to grid
		self.grid.addWidget(self.searchbox,0,0,1,5)
		self.grid.addWidget(self.button,0,5)

		# gene of docs select
		self.gene_button = QRadioButton("Relevant Genes")
		self.gene_button.setChecked(True)
		self.pmid_button = QRadioButton("Relevant PMID list ")
		self.choose_file = QPushButton('Choose File')
		self.choose_file.clicked.connect(self.chooseFile)
		# self.choose_file.setStyleSheet('border-radius: 1px')
		self.filelabel = QLabel(self)

		# Add second row to grid
		self.grid.addWidget(self.gene_button,1,0,1,1)
		self.grid.addWidget(self.pmid_button,1,2,1,1)
		self.grid.addWidget(self.choose_file,1,3,1,2)
		self.grid.addWidget(self.filelabel,1,5,1,5)

		# Recommend label and Third row
		self.mtlabel = QLabel(' ')
		self.mtlabel.setFixedHeight(40)
		self.dummy = QLabel(' ')
		self.grid.addWidget(self.mtlabel,2,0)
		self.grid.addWidget(self.dummy,2,10)

		# Show best MeshTerms
		self.mt1 = QPushButton('')
		self.mt1.setStyleSheet('border: None; text-decoration: underline')
		self.mt1.clicked.connect(self.representative_click)
		self.mt2 = QPushButton(' ')
		self.mt2.setStyleSheet('border: None')
		self.mt2.clicked.connect(self.more_meshterm_click)

		# Add Fourth row to grid
		self.grid.addWidget(self.mt1,3,0,1,8)
		self.grid.addWidget(self.mt2,3,9)
		

		# Top result placeholder buttons
		self.title1 = QPushButton('Title one')
		self.title1.setStyleSheet('border: None; text-decoration: underline; padding-top: 40px')
		self.abs1 = QTextEdit("Abstracts one")
		self.abs1.setReadOnly(True)
		self.title2 = QPushButton('Title two')
		self.title2.setStyleSheet('border: None; text-decoration: underline')
		self.abs2 = QTextEdit("Abstracts two")
		self.abs2.setReadOnly(True)
		self.title3 = QPushButton('Title three')
		self.title3.setStyleSheet('border: None; text-decoration: underline')
		self.abs3 = QTextEdit("Abstracts three")
		self.abs3.setReadOnly(True)

		# Add Fourth row to grid
		self.grid.addWidget(self.title1,4,0,1,5)
		self.grid.addWidget(self.abs1,5,0,2,5)
		self.grid.addWidget(self.title2,7,0,1,5)
		self.grid.addWidget(self.abs2,8,0,2,5)
		self.grid.addWidget(self.title3,11,0,1,5)
		self.grid.addWidget(self.abs3,12,0,2,5)

		# Visualization
		self.vizlabel = QLabel("Visualization: ")
		self.vizlabel.setStyleSheet('padding-top: 40px')
		self.genecloud = QPushButton('Genes cloud')
		self.genecloud.setStyleSheet('border: None; text-decoration: underline')
		self.meshcloud = QPushButton('Mesh cloud')
		self.meshcloud.setStyleSheet('border: None; text-decoration: underline')
		self.grid.addWidget(self.vizlabel,4,6)
		self.grid.addWidget(self.genecloud,5,6)
		self.grid.addWidget(self.meshcloud,6,6)

		self.show()

	@pyqtSlot()
	def search_click(self):
		_textval = self.searchbox.text()
		self._search_term = _textval
		if self.gene_button.isChecked() and self.fileselected:
			if self.fileName:
				goldencorpus = GoldenCorpus(_textval,self.fileName)
				goldencorpus.fetchData()
				self.rel_docs = goldencorpus.get_rel_docs_pmid()
				self.mesh_terms = goldencorpus.get_mesh_terms()
				mesh_explosion = DataForEachMeshTerm(self.mesh_terms,_textval)
				path = mesh_explosion.get_data_foldername(_textval)
				print("sending rel_docs: ",len(self.rel_docs))
				clus = Clusterer(self.rel_docs,path,True,8)
				self.representative_id,self.representative,self.best_mesh_terms_id, self.best_mesh_terms = clus.cluster()
				if self.representative:
					self.updateRepresentativeInformation()
			else:
				print("Error! getting file name")
		elif self.pmid_button.isChecked():
			print("Golden corpus exists..")
		else:
			print("Please select related file..")
	def updateRepresentativeInformation(self):
		self.mtlabel.setText('Recommended search Term: ')
		self.mt1.setText(self.representative)
		self.mt2.setText('More Terms')
		self.mt2.setStyleSheet('border-width: 1px 1px; font-weight: bold')
		pp = PostProcessing()
		tags = pp.term_tagging(self.best_mesh_terms)
		self.tags = QLabel('Tags:')
		self.tags.setStyleSheet('padding-top: 40px')
		self.grid.addWidget(self.tags,7,6)
		row = 8
		col = 6
		c = 0
		if tags:
			for _k, _v in tags:
				self.grid.addWidget(TagButton(_k),row,col)
				row += 1
		else:
			print("No tags!")

	def representative_click(self):
		# text = self.mt1.text()
		# self.searchbox.setText(text)
		self.populateTitleAbs(self.representative_id)

	def populateTitleAbs(self,json_no):
		index = 0
		pp = PostProcessing()
		titles , abstracts = pp.getTitleAbs(index,json_no,self._search_term)
		# print(abstracts)
		self.title1.setText(titles[0])
		self.title2.setText(titles[1])
		self.title3.setText(titles[2])
		self.abs1.setText(abstracts[0])
		self.abs2.setText(abstracts[1])
		self.abs3.setText(abstracts[2])
	
	def more_meshterm_click(self):
		parent = QMainWindow()
		popup = MoreMeshTerms()
		# print(self.best_mesh_terms)
		popup.setupUi(self,parent,self.best_mesh_terms,self.best_mesh_terms_id)
		parent.show()
		parent.exec_()

	def chooseFile(self): 
		if self.fileselected:
			self.filelabel.setText("")
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		self.fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
		if self.fileName:
			self.filelabel.setText(self.fileName)
			self.fileselected = 1;
	
class TagButton(QPushButton):
	def __init__(self,term):
		super(TagButton, self).__init__()
		self.setText(term)
		self.setStyleSheet('border: None; text-decoration: underline')

if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = App()
	sys.exit(app.exec_())
