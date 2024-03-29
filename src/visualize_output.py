import os
import numpy as np
import natsort
import ctypes
import glob

from threading import Thread
from PIL import Image, UnidentifiedImageError
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QGridLayout, \
    QTextEdit, QTableWidget
from PyQt5.QtGui import QPixmap, QIcon, QColor
from PyQt5 import uic
from pydicom import read_file, dcmread
from fpdf import FPDF


# importing libraries
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


def read_dicom_series(directory, filepattern="image_*", target_list=None):
    """ Reads a DICOM Series files in the given directory.
    Only filesnames matching filepattern will be considered"""

    if not os.path.exists(directory) or not os.path.isdir(directory):
        raise ValueError("Given directory does not exist or is a file : " + str(directory))
    print('\tRead Dicom', directory)
    lstFilesDCM = natsort.natsorted(glob.glob(os.path.join(directory, filepattern)))
    print('\tLength dicom series', len(lstFilesDCM))
    # Get ref file
    RefDs = read_file(lstFilesDCM[0])
    # Load dimensions based on the number of rows, columns, and slices (along the Z axis)
    ConstPixelDims = (int(RefDs.Rows), int(RefDs.Columns), len(lstFilesDCM))
    # The array is sized based on 'ConstPixelDims'
    ArrayDicom = np.zeros(ConstPixelDims, dtype=RefDs.pixel_array.dtype)
    dicom_files = []
    # loop through all the DICOM files
    for filenameDCM in lstFilesDCM:
        # read the file
        ds = dcmread(filenameDCM)
        # store the raw image data
        ArrayDicom[:, :, lstFilesDCM.index(filenameDCM)] = ds.pixel_array
        dicom_files.append(ds)
        target_list.append(ds)

    return target_list


def dicom_date_to_str(date):
    year = date[0:4]
    month = date[4:6]
    day = date[6:8]
    return f"{year}-{month}-{day}"


def dicom_to_png(dicom_image, path, filename):
    img = dicom_image.pixel_array.astype(float)  # get image array
    scaled_image = (np.maximum(img, 0) / img.max()) * 255.0
    scaled_image = np.uint8(scaled_image)
    final_image = Image.fromarray(scaled_image)
    # final_image.show()
    try:
        final_image.save(f"{path}/{filename}.png")
    except (FileNotFoundError, UnidentifiedImageError):
        print("Something went wrong while writing image. Check your filename and path")
    return final_image


def read_dicom(mask_path, patient_path, patient_filepattern, mask_filepattern):
    patient_files = []
    mask_files = []
    t1 = Thread(target=read_dicom_series, args=[patient_path, patient_filepattern, patient_files])
    t2 = Thread(target=read_dicom_series, args=[mask_path, mask_filepattern, mask_files])

    t1.start()
    t2.start()

    t1.join()
    t2.join()
    return patient_files, mask_files


# TODO: 1- add copy to clipboard button (checked)
#       2- add buttons functionality for history, home, save
class OutputWindow:
    def __init__(self, mask_path, patient_path, patient_filepattern, mask_filepattern, output_folder):
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        self.title = "Report"
        self.width = screensize[0]
        self.height = screensize[1]
        self.app = QApplication([])
        self.window = QWidget()
        self.window.setWindowTitle("Detection")
        self.dicom_image_index = 0
        self.images = read_dicom(mask_path, patient_path, patient_filepattern, mask_filepattern)
        self.patient_dicom = self.images[0]
        self.mask_dicom = self.images[1]
        self.output_folder = output_folder
        self.algorithms = {"Lung Detection": 1, "River Trauma Detection 1": 1, "River Trauma Detection 2": 1,
                           "River Trauma Detection 3": 1, "Heart Maximized Algorithm": 0, "Brain Scan": 0}

    def create_window(self):
        self.add_layout()
        self.window.showMaximized()
        self.window.show()
        self.app.exec_()

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

    def add_layout(self):
        # Top Bar Layout
        container = QWidget()
        navbar_layout = QHBoxLayout(container)
        home_button = QPushButton('')
        home_icon = QIcon("assets/home.png")
        home_button.setIcon(home_icon)
        home_button.setFlat(True)
        navbar_layout.addWidget(home_button)
        history_button = QPushButton()
        history_icon = QIcon("assets/history.png")
        history_button.setIcon(history_icon)
        history_button.setFlat(True)
        navbar_layout.addWidget(history_button)
        save_button = QPushButton()
        save_icon = QIcon("assets/save.png")
        save_button.setIcon(save_icon)
        save_button.setFlat(True)
        navbar_layout.addWidget(save_button)
        exit_button = QPushButton()
        exit_icon = QIcon("assets/log-out.png")
        exit_button.setIcon(exit_icon)
        exit_button.setFlat(True)
        exit_button.clicked.connect(lambda: self.window.close())
        navbar_layout.addWidget(exit_button)
        container.setStyleSheet("background-color: grey;")
        main_navbar_layout = QVBoxLayout()
        main_navbar_layout.addWidget(container)

        pat_dicom_img = self.patient_dicom[self.dicom_image_index]
        patient_id = pat_dicom_img.data_element("PatientID").value
        patient_name = pat_dicom_img.data_element('PatientName').value
        info_layout = QHBoxLayout()
        # - execution buttons
        exec_layout = QHBoxLayout()
        export_button = QPushButton()
        export_icon = QIcon("assets/export.png")
        export_button.setIcon(export_icon)
        exec_layout.addWidget(export_button)
        exec_button = QPushButton()
        exec_icon = QIcon("assets/round-play-button.png")
        exec_button.setIcon(exec_icon)
        exec_layout.addWidget(exec_button)
        # - patient details
        patient_details_layout = QGridLayout()
        patient_details_layout.addWidget(QLabel("Patient Details"), 0, 0)
        patient_name_layout = QHBoxLayout()
        patient_name_layout.addWidget(QLabel("Patient Name"))
        pat_name_text = QTextEdit(str(pat_dicom_img.data_element("PatientName").value))
        pat_name_text.setFixedHeight(30)
        patient_name_layout.addWidget(pat_name_text)
        patient_details_layout.addLayout(patient_name_layout, 1, 0)
        patient_id_layout = QHBoxLayout()
        patient_id_layout.addWidget(QLabel("Patient ID"))
        pat_id_text = QTextEdit(str(patient_id))
        pat_id_text.setFixedHeight(30)
        patient_id_layout.addWidget(pat_id_text)
        patient_details_layout.addLayout(patient_id_layout, 2, 0)
        pat_date_layout = QHBoxLayout()
        pat_date_layout.addWidget(QLabel("Birth Date"))
        birth_date = dicom_date_to_str(pat_dicom_img.data_element("PatientBirthDate").value)
        pat_date_text = QTextEdit(str(birth_date))
        pat_date_text.setFixedHeight(30)
        pat_date_layout.addWidget(pat_date_text)
        patient_details_layout.addLayout(pat_date_layout, 3, 0)
        study_date_layout = QHBoxLayout()
        study_date_layout.addWidget(QLabel("Study Date"))
        study_date = dicom_date_to_str(pat_dicom_img.data_element("StudyDate").value)
        study_date_text = QTextEdit(str(study_date))
        study_date_text.setFixedHeight(30)
        study_date_layout.addWidget(study_date_text)
        patient_details_layout.addLayout(study_date_layout, 4, 0)
        info_layout.addLayout(patient_details_layout)
        # - Study Description
        study_description_layout = QVBoxLayout()
        study_description_layout.addWidget(QLabel("Study Description"))
        study_description_layout.addWidget(QTextEdit())
        info_layout.addLayout(study_description_layout)
        # - Algorithms Checklist
        algorithms_layout = QVBoxLayout()
        algorithms_layout.addWidget(QLabel("Used Algorithms"))
        checked_algorithms_list = QListWidget()
        checked_algorithms_list.setDragEnabled(True)
        checked_algorithms_list.setAcceptDrops(True)
        checked_algorithms_list.setDragDropOverwriteMode(True)
        checked_algorithms_list.itemClicked.connect(lambda item1: self.toggle_algorithm_status(
                                                                                            item1,
                                                                                            unchecked_algorithms_list,
                                                                                            checked_algorithms_list))
        algorithms_layout.addWidget(checked_algorithms_list)
        algorithms_layout.addWidget(QLabel("Unused Algorithms"))
        unchecked_algorithms_list = QListWidget()
        unchecked_algorithms_list.setAcceptDrops(True)
        unchecked_algorithms_list.setDragEnabled(True)
        unchecked_algorithms_list.itemClicked.connect(lambda item1: self.toggle_algorithm_status(
                                                                                            item1,
                                                                                            unchecked_algorithms_list,
                                                                                            checked_algorithms_list))

        algorithms_layout.addWidget(unchecked_algorithms_list)
        info_layout.addLayout(algorithms_layout)
        for key in self.algorithms.keys():
            item = QListWidgetItem(key)
            if self.algorithms[key] == 1:
                item.setBackground(QColor("#8DF5C1"))
                checked_algorithms_list.addItem(item)
            elif self.algorithms[key] == 0:
                item.setBackground(QColor("#DAF58D"))
                unchecked_algorithms_list.addItem(item)
        # - Report List
        report_layout = QHBoxLayout()
        report_table = QTableWidget()
        report_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        report_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        report_layout.addWidget(report_table)
        cols = ["Organ", "Detection"]
        rows = [["Liver", 4, "Abnormal"], ["Bladder", 2, "Abnormal"], ["Kidneys", 0, "Normal"], ["Lung", 4, "Abnormal"],
                ["Stomach", 4, "Abnormal"], ["Intestines", 1, "Abnormal"], ["Liver", 3, "Abnormal"],
                ["Liver", 0, "Normal"],
                ["Liver", 4, "Abnormal"], ["Liver", 5, "Abnormal"]]

        report_table.setRowCount(10)
        report_table.setColumnCount(len(cols))
        report_table.setHorizontalHeaderLabels(cols)

        # setting output model data in the table
        for column in range(len(cols)):
            for row in range(len(rows)):
                grade = rows[row][1]
                detection = rows[row][2]
                if column == 1:
                    last_col_widget = QWidget()
                    last_col_layout = QHBoxLayout()
                    last_col_widget.setLayout(last_col_layout)
                    last_col_layout.addWidget(QLabel(str(detection)))
                    preview_button = QPushButton()
                    preview_button.clicked.connect(lambda: self.preview_dicom(pat_dicom_img,
                                                                              self.mask_dicom[10], patient_name))
                    eye_img = QIcon("assets/eye.png")
                    preview_button.setIcon(eye_img)
                    preview_button.setFlat(True)
                    last_col_layout.addWidget(preview_button)
                    report_table.setCellWidget(row, column, last_col_widget)
                    self.set_widget_background(last_col_widget, grade)
                else:
                    item = QTableWidgetItem(str(rows[row][column]))
                    # changing color of each row based on its grade
                    self.set_item_background(item, grade)
                    report_table.setItem(row, column, item)  # your contents
        save_button.clicked.connect(
            lambda: self.save(patient_name, patient_id, {"Study Date": study_date,
                                                         "Birth Date": birth_date}))
        # Main layout of the window
        main_layout = QVBoxLayout()
        bottom_layout = QHBoxLayout()
        # bottom_layout.addLayout(dicom_viewer_layout)
        bottom_layout.addLayout(info_layout)
        # bottom_layout.addLayout(report_layout)
        main_layout.addLayout(main_navbar_layout)
        main_layout.addLayout(exec_layout)
        main_layout.addLayout(bottom_layout)
        main_layout.addLayout(report_layout)
        self.window.setLayout(main_layout)

    def save(self, patient_name, patient_id, details: dict):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=15)

        pdf.cell(200, 10, txt="Detection Result", ln=1, align='C')
        pdf.cell(200, 10, txt=f"Patient Name: {patient_name}", ln=2, align='C')
        pdf.cell(200, 10, txt=f"Patient ID: {patient_id}", ln=3, align='C')
        ln_c = 4
        for cell in details.keys():
            pdf.cell(200, 5, txt=f"{cell}: {details[cell]}", ln=ln_c, align='C')
            ln_c += 1
        pdf.cell(200, 5, txt=f"", ln=ln_c, align='C')
        pdf.image(name="temp/images/liver_17^patient_mask.png")
        pdf.output(dest='F', name=f"{self.output_folder}{patient_name}_{patient_id}.pdf")

    @staticmethod
    def preview_dicom(pat_dicom_img, mask_dicom_img, patient_name):
        # Dicom Viewer Section
        dicom_viewer_layout = QVBoxLayout()
        dicom_viewer_layout.addWidget(QLabel("Dicom Preview"))
        dicom_images_widget = QWidget()
        dicom_images_widget.setStyleSheet("background-color: grey;")
        dicom_images_layout = QVBoxLayout(dicom_images_widget)
        dicom_to_png(pat_dicom_img, "temp/images", patient_name)
        pat_image_label = QLabel()
        pat_image = QPixmap(f"temp/images/{patient_name}.png")
        pat_image_label.setPixmap(pat_image)
        dicom_images_layout.addWidget(pat_image_label)
        # - model result
        mask_image_label = QLabel()
        dicom_to_png(mask_dicom_img, "temp/images", f"{patient_name}_mask")
        mask_image = QPixmap(f"temp/images/{pat_dicom_img.data_element('PatientName').value}_mask.png")
        mask_image_label.setPixmap(mask_image)
        dicom_images_layout.addWidget(mask_image_label)
        dicom_viewer_layout.addWidget(dicom_images_widget)

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


# script to be written when user clicks start
if __name__ == "__main__":
    print(os.getcwd() + "\\MASKS_DICOM\\liver")
    print(os.getcwd() + "\\liver 6\\^95020329_20210906")
    ow = OutputWindow(os.getcwd() + "\\..\\MASKS_DICOM\\liver",
                      os.getcwd() + "\\..\\liver 6\\^95020329_20210906",
                      "FILE*", "image_*", "test/output_folder/")
    ow.create_window()
