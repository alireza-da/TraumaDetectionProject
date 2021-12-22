import os
import numpy as np
import natsort
import ctypes
import glob

from matplotlib import pyplot as plt
from PIL import Image
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QGridLayout, \
    QTextEdit
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5 import uic
from pydicom import read_file, dcmread


def imshow(*args, **kwargs):
    """ Handy function to show multiple plots in on row, possibly with different cmaps and titles
    Usage:
    imshow(img1, title="myPlot")
    imshow(img1,img2, title=['title1','title2'])
    imshow(img1,img2, cmap='hot')
    imshow(img1,img2,cmap=['gray','Blues']) """
    cmap = kwargs.get('cmap', 'gray')
    title = kwargs.get('title', '')
    if len(args) == 0:
        raise ValueError("No images given to imshow")
    elif len(args) == 1:
        plt.title(title)
        plt.imshow(args[0], interpolation='none')
    else:
        n = len(args)
        if type(cmap) == str:
            cmap = [cmap] * n
        if type(title) == str:
            title = [title] * n
        plt.figure(figsize=(n * 5, 10))
        for i in range(n):
            plt.subplot(1, n, i + 1)
            plt.title(title[i])
            plt.imshow(args[i], cmap[i])
    plt.show()


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
    dicom_files = []
    # loop through all the DICOM files
    for filenameDCM in lstFilesDCM:
        # read the file
        ds = dcmread(filenameDCM)
        # store the raw image data
        ArrayDicom[:, :, lstFilesDCM.index(filenameDCM)] = ds.pixel_array
        dicom_files.append(ds)

    return dicom_files


def dicom_date_to_str(date):
    year = date[0:4]
    month = date[4:6]
    day = date[6:8]
    return f"{year}-{month}-{day}"

# TODO particular except clause
def dicom_to_png(dicom_image, path, filename):
    img = dicom_image.pixel_array.astype(float)  # get image array
    scaled_image = (np.maximum(img, 0) / img.max()) * 255.0
    scaled_image = np.uint8(scaled_image)
    final_image = Image.fromarray(scaled_image)
    # final_image.show()
    try:
        final_image.save(f"{path}/{filename}.png")
    except:
        print("Something went wrong while writing image. Check your filename and path")
    return final_image


def read_dicom(mask_path, patient_path, patient_filepattern, mask_filepattern):
    patient_files = read_dicom_series(patient_path, patient_filepattern)
    mask_files = read_dicom_series(mask_path, mask_filepattern)
    return patient_files, mask_files


# TODO 1- add copy to clipboard button
#      2- add save button

class OutputWindow:
    def __init__(self, mask_path, patient_path, patient_filepattern, mask_filepattern):
        user32 = ctypes.windll.user32
        screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        self.title = "Report"
        self.width = screensize[0]
        self.height = screensize[1]
        self.app = QApplication([])
        self.window = QWidget()
        self.dicom_image_index = 0
        self.images = read_dicom(mask_path, patient_path, patient_filepattern, mask_filepattern)
        self.patient_dicom = self.images[0]
        self.mask_dicom = self.images[1]

    def create_window(self):
        self.add_layout()
        self.window.showMaximized()
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
        main_navbar_layout.addWidget(container)
        # Dicom Viewer Section
        dicom_viewer_layout = QVBoxLayout()
        dicom_viewer_layout.addWidget(QLabel("Dicom Preview"))
        dicom_images_widget = QWidget()
        dicom_images_widget.setStyleSheet("background-color: grey;")
        dicom_images_layout = QVBoxLayout(dicom_images_widget)
        # - convert dicom to png
        pat_dicom_img = self.patient_dicom[self.dicom_image_index]
        patient_id = pat_dicom_img.data_element("PatientID").value
        patient_name = pat_dicom_img.data_element('PatientName').value
        dicom_to_png(pat_dicom_img, "temp/images", patient_name)
        pat_image_label = QLabel()
        pat_image = QPixmap(f"temp/images/{patient_name}.png")
        pat_image_label.setPixmap(pat_image)
        dicom_images_layout.addWidget(pat_image_label)
        # - model result
        mask_image_label = QLabel()
        dicom_to_png(self.mask_dicom[10], "temp/images", f"{patient_name}_mask")
        mask_image = QPixmap(f"temp/images/{pat_dicom_img.data_element('PatientName').value}_mask.png")
        mask_image_label.setPixmap(mask_image)
        dicom_images_layout.addWidget(mask_image_label)
        dicom_viewer_layout.addWidget(dicom_images_widget)
        # Report Section
        report_layout = QVBoxLayout()
        report_layout.addWidget(QLabel("Report"))
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
        pat_date_layout.addWidget(QLabel("Study Date"))
        pat_date_text = QTextEdit(str(dicom_date_to_str(pat_dicom_img.data_element("StudyDate").value)))
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
        main_layout = QVBoxLayout()
        bottom_layout = QHBoxLayout()
        bottom_layout.addLayout(dicom_viewer_layout)
        bottom_layout.addLayout(report_layout)
        main_layout.addLayout(main_navbar_layout)
        main_layout.addLayout(bottom_layout)
        self.window.setLayout(main_layout)


# script to be written when user clicks start
if __name__ == "__main__":
    ow = OutputWindow("C:\\Users\\rasta\\Downloads\\Compressed\\3Dircadb1.17\\3Dircadb1.17\\MASKS_DICOM\\liver",
                      "C:\\Users\\rasta\\Downloads\\Compressed\\3Dircadb1.17\\3Dircadb1.17\\PATIENT_DICOM",
                      "image_*", "image_*")
    ow.create_window()
