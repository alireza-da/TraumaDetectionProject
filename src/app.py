import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5 import uic, QtGui
from functools import partial
from DicomFileHandler import DicomHandler as DH
import Type as TP


class MyApp(QMainWindow):
    def __init__(self, isReadFileMode):
        super().__init__()
        uic.loadUi('./app.ui', self)
        self.manual_file_path_button.clicked.connect(self.getFileName)
        self.manual_result_path_button.clicked.connect(partial(self.getDirectory, self.manual_result_path_text))
        self.manual_start.clicked.connect(self.workWithFile)

        self.file_name = ''
        self.is_manual_file_path_set = False
        self.is_manual_folder_result_set = False

        self.isReadFileMode = isReadFileMode

        self.setWindowTitle("trauma")
        self.setWindowIcon(QtGui.QIcon("./logo.png"))

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
                type = DH.getFileType(self.manual_file_path_text.text())
                if type == TP.Type.DICOM:
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

        file, self.file_name = DH.readDicomPydicom(self.manual_file_path_text.text())
        return file

    def readFileByte(self):
        file, self.file_name = DH.readByte(self.manual_file_path_text.text())
        return file

    def readFileNifti(self):
        file, self.file_name = DH.readNifti(self.manual_file_path_text.text())
        return file

    def writeFilePyDicom(self, result):
        DH.writeFilePyDicom(self.manual_result_path_text.text(), self.file_name, result)

    def writeFileByte(self, result):
        DH.writeDicomByte(self.manual_result_path_text.text(), self.file_name, result)

    def workWithFileDone(self):
        QMessageBox.information(self, "job done", "the job has done")

    def workingWithFIleError(self):
        QMessageBox.warning(self, "something went wrong", "we cant work with file")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = MyApp(True)
    gui.show()

    try:
        sys.exit(app.exec_())
    except:
        print('closing window...')
