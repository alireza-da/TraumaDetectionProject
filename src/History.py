import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton
from PyQt5 import uic, QtGui, QtCore
from app import MyApp


class History(QMainWindow):
    def __init__(self):
        super().__init__()
        # print(os.listdir())
        uic.loadUi('history.ui', self)
        self.setButton()
        self.setTable()
        self.setWindowTitle("History")
        self.setWindowIcon(QtGui.QIcon("assets/logo.png"))
        self.MyApp = None

    def setButton(self):
        self.home_button.setIcon(QtGui.QIcon('assets/home.png'))
        self.home_button.setIconSize(QtCore.QSize(24, 24))
        self.home_button.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.home_button.clicked.connect(self.homePress)

    def setTable(self):
        width = self.table.frameGeometry().width()
        col0_size = 320
        col1_size = 200
        col3_size = 320
        col2_size = width - (col0_size + col1_size + col3_size) - 21
        self.table.setColumnWidth(0, col0_size)
        self.table.setColumnWidth(1, col1_size)
        self.table.setColumnWidth(2, col2_size)
        self.table.setColumnWidth(3, col3_size)

        self.addRows()

    def addRows(self):
        rows = [{"patient": "John Doe", "Date": "2022/23/1", "Status": "Abnormal", "Study": "Lung - Liver"},
                {"patient": "Jane Doe", "Date": "2022/23/1", "Status": "Abnormal", "Study": "Brain - Heart"},
                {"patient": "Johnathon Doe ", "Date": "2022/23/1", "Status": "Normal", "Study": "Lung - Liver"}]

        self.table.setRowCount(len(rows))
        for index, row in enumerate(rows):
            self.table.setItem(index, 0, QTableWidgetItem(row["patient"]))
            self.table.setItem(index, 1, QTableWidgetItem(row["Date"]))
            self.table.setItem(index, 2, QTableWidgetItem(row["Status"]))
            self.table.setItem(index, 3, QTableWidgetItem(row["Status"]))
            for i in range(0, 4):
                self.table.item(index, i).setBackground(QtGui.QColor(222, 217, 217))
                self.table.item(index, i).setTextAlignment(QtCore.Qt.AlignCenter)

    def homePress(self):
        if self.MyApp is None:
            self.MyApp = MyApp(False)
        self.MyApp.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = History()
    gui.showMaximized()
    # gui.show()

    try:
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
        print('closing window...')
