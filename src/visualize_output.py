import os
import numpy as np
import natsort
import ctypes
import glob
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QGridLayout, \
    QTextEdit
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5 import uic
from pydicom import read_file


def read_dicom_series(directory, filepattern="image_*"):
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

    # loop through all the DICOM files
    for filenameDCM in lstFilesDCM:
        # read the file
        ds = read_file(filenameDCM)
        # store the raw image data
        ArrayDicom[:, :, lstFilesDCM.index(filenameDCM)] = ds.pixel_array

    return ArrayDicom


class OutputWindow:
    def __init__(self):
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        self.title = "Report"
        self.width = screensize[0]
        self.height = screensize[1]
        self.app = QApplication([])
        self.window = QWidget()

    def create_window(self):
        self.add_layout()
        self.window.show()
        self.app.exec_()

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
        exit_button = QPushButton()
        exit_icon = QIcon("assets/log-out.png")
        exit_button.setIcon(exit_icon)
        exit_button.setFlat(True)
        navbar_layout.addWidget(exit_button)
        container.setStyleSheet("background-color: grey;")
        main_navbar_layout = QVBoxLayout()
        container.setFixedWidth(self.width)
        main_navbar_layout.addWidget(container)
        # Dicom Viewer Section
        dicom_viewer_layout = QVBoxLayout()
        dicom_viewer_layout.addWidget(QLabel("Dicom Preview"))
        # Report Section
        report_layout = QVBoxLayout()
        report_layout.addWidget(QLabel("Report"))
        images_viewer_layout = QVBoxLayout()

        # - patient details
        patient_details_layout = QGridLayout()
        patient_details_layout.addWidget(QLabel("Patient Details"), 0, 0)
        patient_name_layout = QHBoxLayout()
        patient_name_layout.addWidget(QLabel("Patient Name"))
        pat_name_text = QTextEdit("Antonio Johansson")
        pat_name_text.setFixedHeight(30)
        patient_name_layout.addWidget(pat_name_text)
        patient_details_layout.addLayout(patient_name_layout, 1, 0)
        patient_id_layout = QHBoxLayout()
        patient_id_layout.addWidget(QLabel("Patient ID"))
        pat_id_text = QTextEdit(str(22111010))
        pat_id_text.setFixedHeight(30)
        patient_id_layout.addWidget(pat_id_text)
        patient_details_layout.addLayout(patient_id_layout, 2, 0)
        pat_date_layout = QHBoxLayout()
        pat_date_layout.addWidget(QLabel("Date"))
        pat_date_text = QTextEdit("2021-21-12")
        pat_date_text.setFixedHeight(30)
        pat_date_layout.addWidget(pat_date_text)
        patient_details_layout.addLayout(pat_date_layout, 3, 0)
        report_layout.addLayout(patient_details_layout)
        # - detection details
        detection_layout = QVBoxLayout()
        detection_layout.addWidget(QLabel("Detection"))
        # - model result
        detection_text = QTextEdit("1- A tumor has been detected in liver.\n 2- A tumor has been detected in liver.\n"
                                   "Summary: \n Liver has two tumors.")
        detection_text.setFixedHeight(100)
        detection_layout.addWidget(detection_text)
        report_layout.addLayout(detection_layout)
        # - status
        status_layout = QVBoxLayout()
        status_layout_label = QHBoxLayout()
        status_layout_label.addWidget(QLabel("Status"))
        status_image_label = QLabel()
        status_image = QPixmap("assets/red_circle.png")
        status_image_label.setPixmap(status_image)
        status_layout_label.addWidget(status_image_label)
        status_layout.addLayout(status_layout_label)
        status_text = QTextEdit("Needs surgery. Needs ICU Reservation.")
        status_text.setFixedHeight(100)
        status_layout.addWidget(status_text)
        report_layout.addLayout(status_layout)
        # Main layout of the window
        main_layout = QGridLayout()
        main_layout.addLayout(main_navbar_layout, 0, 0)
        main_layout.addLayout(dicom_viewer_layout, 1, 0)
        main_layout.addLayout(report_layout, 1, 1)
        self.window.setLayout(main_layout)

    def visualize_report(self, mask_path, patient_path):
        patient_files = read_dicom_series(patient_path)
        mask_files = read_dicom_series(mask_path)
        print(self.window)


# script to be written when user clicks start
if __name__ == "__main__":
    ow = OutputWindow()
    ow.create_window()
    ow.visualize_report("C:\\Users\\rasta\\Downloads\\Compressed\\3Dircadb1.17\\3Dircadb1.17\\MASKS_DICOM\\liver",
                        "C:\\Users\\rasta\\Downloads\\Compressed\\3Dircadb1.17\\3Dircadb1.17\\PATIENT_DICOM")
