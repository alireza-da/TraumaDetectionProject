import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget,QMainWindow,QFileDialog,QMessageBox
from PyQt5 import uic
from functools import partial
import pydicom


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.file_name = '';
        uic.loadUi('./app.ui',self)
        self.manual_file_path_button.clicked.connect(self.getFileName)
        self.manual_result_path_button.clicked.connect(partial(self.getDirectory,self.manual_result_path_text))
        self.manual_start.clicked.connect(self.workWithFile)

    
    def getFileName(self):
        file_filter = 'Data file (*.dcm)'
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption='select a file',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter=file_filter
        )
        if response[0]:
            self.manual_file_path_text.setText(response[0])

    def getDirectory(self,the_label):
        response = QFileDialog.getExistingDirectory(
            parent=self,
            caption='select a folder',
            directory=os.getcwd()
        )

        if response:
            the_label.setText(response)


    def workWithFile(self):
       
        try:
            file = self.readFile();
            #work with file
            self.writeFile(file)
            self.workWithFileDone()
        except Exception as e:
            self.workingWithFIleError()
    
    def readFile(self):
        file =   pydicom.dcmread(self.manual_file_path_text.text())
        self.file_name = self.manual_file_path_text.text().split('/')[-1] + "_result"
        return file
        

    def writeFile(self,result):
        result.save_as(self.manual_result_path_text.text()+"/"+self.file_name)
        
    def workWithFileDone(self):
        QMessageBox.warning(self, "job done", "the job has done")


    def workingWithFIleError(self):
        QMessageBox.warning(self, "something went wrong", "we cant work with file")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    gui = MyApp()
    gui.show()


    try:
        sys.exit(app.exec_())
    except:
        print('closing window...')