from fileinput import close
import sys
import os

from PyQt5.QtGui import QColor, QPixmap, QCursor, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton, QListWidgetItem, QWidget, \
    QHBoxLayout, QVBoxLayout, QLabel, QTextEdit
from PyQt5 import uic, QtGui, QtCore
from fpdf import FPDF
from visualize_output import dicom_to_png, read_dicom, dicom_date_to_str
from History import History
from app import MyApp
from random import randint
from visualize_output_v2 import OutputWindow


class Page2(QMainWindow):
    def __init__(self, isReadFileMode, mask_path, patient_path, patient_filepattern, mask_filepattern, output_folder):
        self.mask_path = mask_path
        self.patient_path = patient_path
        self.patient_filepattern = patient_filepattern
        self.mask_filepattern = mask_filepattern
        self.images = read_dicom(mask_path, patient_path, patient_filepattern, mask_filepattern)
        self.outputWindow = OutputWindow(mask_path, patient_path,
                                         patient_filepattern, mask_filepattern, output_folder)
        self.patient_dicom = self.images[0]
        self.mask_dicom = self.images[1]
        self.output_folder = output_folder
        self.algorithms = {"Lung Detection": 1, "River Trauma Detection 1": 1, "River Trauma Detection 2": 1,
                           "River Trauma Detection 3": 1, "Heart Maximized Algorithm": 0, "Brain Scan": 0}
        self.patient_name = self.patient_dicom[0].data_element('PatientName').value
        self.patient_id = self.patient_dicom[0].data_element("PatientID").value
        self.patient_bd = dicom_date_to_str(self.patient_dicom[0].data_element("PatientBirthDate").value)
        self.rows = []
        self.rows_copy = [{"organ": "Liver", "grade": 1, "status": "Abnormal"},
                          {"organ": "Lung", "grade": 2, "status": "Abnormal"},
                          {"organ": "Heart", "grade": 0, "status": "Normal"}]

        super().__init__()
        # print(os.listdir())

        uic.loadUi('page2.ui', self)
        self.setButton()
        self.setTable()
        self.setAlgorithmList()
        self.setPatientDetails()
        self.textBrowser.setText("Heart - Lung - Liver")
        self.setWindowTitle("Trauma")
        self.setWindowIcon(QtGui.QIcon("assets/logo.png"))
        self.historyApp = None
        self.MyApp = None

    def setPatientDetails(self):
        self.patient_id_text.setText(self.patient_id)
        self.patient_name_text.setText(str(self.patient_name))
        self.patient_bd_text.setText(str(self.patient_bd))

    def save(self, details: dict):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=15)

        pdf.cell(200, 10, txt="Detection Result", ln=1, align='C')
        pdf.cell(200, 10, txt=f"Patient Name: {self.patient_name}", ln=2, align='C')
        pdf.cell(200, 10, txt=f"Patient ID: {self.patient_id}", ln=3, align='C')
        ln_c = 4
        for cell in details.keys():
            pdf.cell(200, 5, txt=f"{cell}: {details[cell]}", ln=ln_c, align='C')
            ln_c += 1
        pdf.cell(200, 5, txt=f"", ln=ln_c, align='C')
        pdf.image(name="temp/images/liver_17^patient_mask.png")
        pdf.output(dest='F', name=f"{self.output_folder}/{self.patient_name}_{self.patient_id}.pdf")

    def toggle_algorithm_status(self, algorithm: QListWidgetItem, unchecked, checked):
        key = algorithm.text()
        if self.algorithms[key] == 1:
            checked.takeItem(checked.currentRow())
            algorithm.setBackground(QColor("#DAF58D"))
            unchecked.addItem(algorithm)
            self.algorithms[key] = 0
        else:
            unchecked.takeItem(unchecked.currentRow())
            algorithm.setBackground(QColor("#8DF5C1"))
            checked.addItem(algorithm)
            self.algorithms[key] = 1

    def setAlgorithmList(self):
        # self.list_used_algo.addItems(["first", "second"])
        # self.list_unused_algo.addItems(["third"])
        # algorithms_layout.addWidget(QLabel("Used Algorithms"))
        self.list_used_algo.setDragEnabled(True)
        self.list_used_algo.setAcceptDrops(True)
        # self.list_used_algo.setDragDropOverwriteMode(True)
        self.list_used_algo.itemClicked.connect(lambda item1: self.toggle_algorithm_status(
            item1,
            self.list_unused_algo,
            self.list_used_algo))
        # algorithms_layout.addWidget(checked_algorithms_list)
        # algorithms_layout.addWidget(QLabel("Unused Algorithms"))
        # unchecked_algorithms_list = QListWidget()
        self.list_unused_algo.setAcceptDrops(True)
        self.list_unused_algo.setDragEnabled(True)
        self.list_unused_algo.itemClicked.connect(lambda item1: self.toggle_algorithm_status(
            item1,
            self.list_unused_algo,
            self.list_used_algo))

        # algorithms_layout.addWidget(unchecked_algorithms_list)
        # info_layout.addLayout(algorithms_layout)
        for key in self.algorithms.keys():
            item = QListWidgetItem(key)
            if self.algorithms[key] == 1:
                item.setBackground(QColor("#8DF5C1"))
                self.list_used_algo.addItem(item)
            elif self.algorithms[key] == 0:
                item.setBackground(QColor("#DAF58D"))
                self.list_unused_algo.addItem(item)

    def preview_dicom(self, pat_dicom_img, mask_dicom_img, patient_name, organ):
        self.outputWindow.create_window()
        # self.window = QWidget()
        # self.window.setWindowTitle(f"{self.patient_name} - {organ}")
        # # Dicom Viewer Section
        # dicom_viewer_layout = QVBoxLayout()
        # dicom_viewer_layout.addWidget(QLabel("Dicom Preview"))
        # dicom_images_widget = QWidget()
        # dicom_images_widget.setStyleSheet("background-color: grey;")
        # dicom_images_layout = QHBoxLayout(dicom_images_widget)
        # dicom_to_png(pat_dicom_img, "temp/images", patient_name)
        # pat_image_label = QLabel()
        # pat_image = QPixmap(f"temp/images/{patient_name}.png")
        # pat_image_label.setPixmap(pat_image)
        # dicom_images_layout.addWidget(pat_image_label)
        # # - model result
        # mask_image_label = QLabel()
        # dicom_to_png(mask_dicom_img, "temp/images", f"{patient_name}_mask")
        # mask_image = QPixmap(f"temp/images/{pat_dicom_img.data_element('PatientName').value}_mask.png")
        # mask_image_label.setPixmap(mask_image)
        # dicom_images_layout.addWidget(mask_image_label)
        # dicom_viewer_layout.addWidget(dicom_images_widget)
        # self.window.setLayout(dicom_viewer_layout)
        # self.window.show()

    def setTable(self):
        width = self.table.frameGeometry().width()
        col0_size = 300
        col2_size = 200
        col1_size = width - (col0_size + col2_size) - 30
        self.table.setColumnWidth(0, col0_size)
        self.table.setColumnWidth(1, col1_size)
        self.table.setColumnWidth(2, col2_size)
        cols = ["Organ", "Status", "Preview"]
        self.table.setHorizontalHeaderLabels(cols)
        self.table.setColumnCount(len(cols))
        self.table.setHorizontalHeaderLabels(cols)
        # self.table.setColumns(cols)

        self.addRows()

    def randomize_run(self):
        self.setCursor(QCursor(QtCore.Qt.CursorShape.BusyCursor))
        for _ in self.rows_copy:
            is_remove = randint(0, 2)
            index = randint(0, len(self.rows_copy) - 1)
            if is_remove == 1 and len(self.rows) > 1 and index < len(self.rows):
                self.rows.remove(self.rows[index])
            if is_remove == 0:
                self.rows.append(self.rows_copy[index])

        if len(self.rows_copy) == 0:
            self.rows.append(self.rows_copy[0])

        # The most stupid script i ve ever written
        i = 0
        while i < 20000000:
            i += 1

        self.setCursor(QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        self.addRows()

    def addRows(self):
        cols = ["Organ", "Status", "Preview"]
        self.table.clear()
        self.table.setRowCount(len(self.rows))
        self.table.setHorizontalHeaderLabels(cols)
        for column in cols:
            for row in range(len(self.rows)):
                grade = self.rows[row]["grade"]
                col_ind = cols.index(column)
                if column == "Preview":
                    last_col_widget = QWidget()
                    last_col_layout = QHBoxLayout()
                    last_col_widget.setLayout(last_col_layout)
                    # last_col_layout.addWidget(QLabel(str(status)))
                    preview_button = QPushButton()
                    pat_dicom_img = self.patient_dicom[0]
                    patient_name = pat_dicom_img.data_element('PatientName').value
                    preview_button.clicked.connect(lambda: self.preview_dicom(pat_dicom_img,
                                                                              self.mask_dicom[10], patient_name
                                                                              , self.rows[row]["organ"]))
                    eye_img = QIcon("assets/eye.png")
                    preview_button.setIcon(eye_img)
                    preview_button.setFlat(True)
                    last_col_layout.addWidget(preview_button)
                    self.table.setCellWidget(row, col_ind, last_col_widget)
                    self.set_widget_background(last_col_widget, grade)
                else:
                    item = QTableWidgetItem(str(self.rows[row][column.lower()]))
                    # changing color of each row based on its grade
                    self.set_item_background(item, grade)
                    self.table.setItem(row, col_ind, item)  # your contents

    @staticmethod
    def set_item_background(item, grade):
        red_color = QColor('#F58D8D')
        green_color = QColor("#8DF5C1")
        if grade > 1:
            item.setBackground(red_color)
        elif grade == 1:
            item.setBackground(red_color)
        else:
            item.setBackground(green_color)

    @staticmethod
    def set_widget_background(item, grade):
        if grade > 1:
            item.setStyleSheet("background-color: #F58D8D;")
        elif grade == 1:
            item.setStyleSheet("background-color: #F58D8D;")
        else:
            item.setStyleSheet("background-color: #8DF5C1;")

    @staticmethod
    def getRGBcolor(colorNumber):
        red_color = QColor('#F58D8D')
        green_color = QColor("#8DF5C1")
        # colorNumber -> 1 :red , 2 :green , else:yellow
        if colorNumber >= 1:
            return red_color
        elif colorNumber == 0:
            return green_color
        else:
            return QColor(245, 245, 141)

    @staticmethod
    def getBackgroundColortext(colorNumber):
        # colorNumber -> 1 :red , 2 :green , else:yellow
        if colorNumber >= 1:
            return "background-color: rgba(245, 141, 141);"
        elif colorNumber == 0:
            return "background-color: rgba(141, 245, 193);"
        else:
            return "background-color: rgba(245, 245, 141);"

    def setButton(self):
        self.home_button.setIcon(QtGui.QIcon('assets/home.png'))
        self.home_button.setIconSize(QtCore.QSize(24, 24))
        self.home_button.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.home_button.clicked.connect(self.homePress)

        self.history_button.setIcon(QtGui.QIcon('assets/history.png'))
        self.history_button.setIconSize(QtCore.QSize(24, 24))
        self.history_button.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.history_button.clicked.connect(self.historyPress)

        self.exit_button.setIcon(QtGui.QIcon('assets/log-out.png'))
        self.exit_button.setIconSize(QtCore.QSize(24, 24))
        self.exit_button.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.exit_button.clicked.connect(self.close)

        self.save_button.setIcon(QtGui.QIcon('assets/save.png'))
        self.save_button.setIconSize(QtCore.QSize(24, 24))
        self.save_button.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.save_button.clicked.connect(lambda: self.save(dict()))

        self.ok_button.setIcon(QtGui.QIcon('assets/round-play-button.png'))
        self.ok_button.setIconSize(QtCore.QSize(24, 24))
        self.ok_button.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.ok_button.clicked.connect(self.randomize_run)

    def historyPress(self):
        if self.historyApp is None:
            self.historyApp = History()
        self.historyApp.show()
        self.close()

    def homePress(self):
        if self.MyApp is None:
            self.MyApp = MyApp(False)
        self.MyApp.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = Page2(False, os.getcwd() + "\\..\\MASKS_DICOM\\liver",
                os.getcwd() + "\\..\\PATIENT_DICOM",
                "image_*", "image_*", "test/output_folder")
    # gui.showMaximized()
    gui.show()

    try:
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
        print('closing window...')
