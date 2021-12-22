import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5 import uic, QtGui,QtCore
from functools import partial
from DicomFileHandler import DicomHandler as dH
import Type as tP


class MyApp(QMainWindow):
    def __init__(self, isReadFileMode):
        super().__init__()
        print( os.listdir())
        uic.loadUi('src/app.ui', self)
        self.manual_file_path_button.clicked.connect(self.getFileName)
        self.manual_result_path_button.clicked.connect(partial(self.getDirectory, self.manual_result_path_text))
        self.manual_start.clicked.connect(self.workWithFile)

        self.file_name = ''
        self.is_manual_file_path_set = False
        self.is_manual_folder_result_set = False

        self.isReadFileMode = isReadFileMode

        self.setWindowTitle("Trauma")
        self.setWindowIcon(QtGui.QIcon("./src/assets/logo.png"))


        self.setUpSidePageButton()
        
    def setUpSidePageButton(self):


        self.logo_home.setIcon(QtGui.QIcon('./src/assets/home.png'))
        self.logo_home.setIconSize(QtCore.QSize(24,24)) 
        self.logo_home.setStyleSheet("background-color: rgba(255, 255, 255, 0);");
        self.logo_home.clicked.connect(self.homePress)

        self.logo_history.setIcon(QtGui.QIcon('./src/assets/history.png'))
        self.logo_history.setIconSize(QtCore.QSize(24,24)) 
        self.logo_history.setStyleSheet("background-color: rgba(255, 255, 255, 0);");
        self.logo_history.clicked.connect(self.histroryPress)


        self.logo_back.setIcon(QtGui.QIcon('./src/assets/log-out.png'))
        self.logo_back.setIconSize(QtCore.QSize(24,24)) 
        self.logo_back.setStyleSheet("background-color: rgba(255, 255, 255, 0);");
        self.logo_back.clicked.connect(self.close)


        self.logo_help.setIcon(QtGui.QIcon('./src/assets/help.png'))
        self.logo_help.setIconSize(QtCore.QSize(24,24)) 
        self.logo_help.setStyleSheet("background-color: rgba(255, 255, 255, 0);");
        self.logo_help.clicked.connect(self.helpPress)


        self.logo_email.setIcon(QtGui.QIcon('./src/assets/email.png'))
        self.logo_email.setIconSize(QtCore.QSize(24,24)) 
        self.logo_email.setStyleSheet("background-color: rgba(255, 255, 255, 0);");
        self.logo_email.clicked.connect(self.emailPress)


    def homePress(self):
        pass
    
    def histroryPress(self):
        pass

    def helpPress(self):
        msgBox = QMessageBox()
        msgBox.setWindowIcon(QtGui.QIcon("./src/assets/logo.png"))
        msgBox.setText("1.something \n2.something \n3.something\n                                            ")
        msgBox.setWindowTitle("help")
        msgBox.setFixedWidth(600)
        msgBox.exec()
        

    
    def emailPress(self):
        msgBox = QMessageBox()
        msgBox.setWindowIcon(QtGui.QIcon("./src/assets/logo.png"))
        msgBox.setText("email\nphone\naddress\n                                            ")
        msgBox.setWindowTitle("contact")
        msgBox.setFixedWidth(600)
        msgBox.exec()



    def getFileName(self):
        file_filter = 'Data file (*.dcm *.nii)'
        response = QFileDialog.getOpenFileName(
            parent=self,
            caption='select a file',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter=file_filter
        )
        if response[0]:
            self.manual_file_path_text.setText(response[0])
            self.is_manual_file_path_set = True

    def getDirectory(self, the_label):
        response = QFileDialog.getExistingDirectory(
            parent=self,
            caption='select a folder',
            directory=os.getcwd()
        )

        if response:
            the_label.setText(response)
            self.is_manual_folder_result_set = True

    def workWithFile(self):
        if (not self.is_manual_file_path_set) and (not self.is_manual_folder_result_set):
            QMessageBox.warning(self, "lack of information", "you must fill file path and result folder ")
            return
        elif not self.is_manual_file_path_set:
            QMessageBox.warning(self, "lack of information", "you must fill file path")
            return
        elif not self.is_manual_folder_result_set:
            QMessageBox.warning(self, "lack of information", "you must fill result folder")
            return

        try:
            if self.isReadFileMode:
                type = dH.getFileType(self.manual_file_path_text.text())
                if type == tP.Type.DICOM:
                    file = self.readFilePyDicom();
                    # work with file
                    self.writeFilePyDicom(file)

                else:
                    file = self.readFileNifti()
                    print(file)
                    # work with nifti
                    # todo

            else:
                file = self.readFileByte()
                # work with file if it is nifti
                self.writeFileByte(b''.join(file))
            self.workWithFileDone()
        except Exception as e:
            print(e)
            self.workingWithFIleError()

    def readFilePyDicom(self):

        file, self.file_name = dH.readDicomPydicom(self.manual_file_path_text.text())
        return file

    def readFileByte(self):
        file, self.file_name = dH.readByte(self.manual_file_path_text.text())
        return file

    def readFileNifti(self):
        file, self.file_name = dH.readNifti(self.manual_file_path_text.text())
        return file

    def writeFilePyDicom(self, result):
        dH.writeFilePyDicom(self.manual_result_path_text.text(), self.file_name, result)

    def writeFileByte(self, result):
        dH.writeDicomByte(self.manual_result_path_text.text(), self.file_name, result)

    def workWithFileDone(self):
        QMessageBox.information(self, "job done", "the job has done")

    def workingWithFIleError(self):
        QMessageBox.warning(self, "something went wrong", "we cant work with file")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = MyApp(False)
    gui.show()

    try:
        sys.exit(app.exec_())
    except:
        print('closing window...')
