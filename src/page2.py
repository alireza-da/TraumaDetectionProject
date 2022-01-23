from fileinput import close
import sys
import os

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QPushButton, QListWidgetItem, QWidget, \
    QHBoxLayout
from PyQt5 import uic, QtGui, QtCore

from History import History
from app import MyApp


class Page2(QMainWindow):
    def __init__(self, isReadFileMode):
        super().__init__()
        # print(os.listdir())
        uic.loadUi('page2.ui', self)
        self.setButton()
        self.setTable()
        self.setAlgorithmList()
        self.historyApp = None
        self.MyApp = None
        self.algorithms = {"Lung Detection": 1, "River Trauma Detection 1": 1, "River Trauma Detection 2": 1,
                           "River Trauma Detection 3": 1, "Heart Maximized Algorithm": 0, "Brain Scan": 0}

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
        self.list_used_algo.setDragDropOverwriteMode(True)
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
            self.list_unused_algo))

        # algorithms_layout.addWidget(unchecked_algorithms_list)
        # info_layout.addLayout(algorithms_layout)
        self.algorithms = {"Lung Detection": 1, "River Trauma Detection 1": 1, "River Trauma Detection 2": 1,
                           "River Trauma Detection 3": 1, "Heart Maximized Algorithm": 0, "Brain Scan": 0}
        for key in self.algorithms.keys():
            item = QListWidgetItem(key)
            if self.algorithms[key] == 1:
                item.setBackground(QColor("#8DF5C1"))
                self.list_used_algo.addItem(item)
            elif self.algorithms[key] == 0:
                item.setBackground(QColor("#DAF58D"))
                self.list_unused_algo.addItem(item)

    def setTable(self):
        width = self.table.frameGeometry().width()
        col0_size = 300
        col2_size = 200
        col1_size = width - (col0_size + col2_size) - 30
        self.table.setColumnWidth(0, col0_size)
        self.table.setColumnWidth(1, col1_size)
        self.table.setColumnWidth(2, col2_size)

        self.addRows()

    def addRows(self):
        rows = [{"organs": "Liver", "grade": 1, "detection": "Abnormal"},
                {"organs": "Lung", "grade": 2, "detection": "Abnormal"},
                {"organs": "Heart", "grade": 0, "detection": "Normal"}]

        self.table.setRowCount(3)
        for index, row in enumerate(rows):
            self.table.setItem(index, 0, QTableWidgetItem(row["organs"]))
            self.table.setItem(index, 1, QTableWidgetItem(row["detection"]))
            last_col_widget = QWidget()
            last_col_layout = QHBoxLayout()
            last_col_widget.setLayout(last_col_layout)
            btn = QPushButton('')
            btn.setIcon(QtGui.QIcon('assets/eye.png'))
            btn.setFlat(True)
            # btn.setIconSize(QtCore.QSize(12, 12))
            last_col_layout.addWidget(btn)
            self.table.setCellWidget(index, 2, last_col_widget)

            for i in range(0, 3):
                grade = row["grade"]
                if i == 2:
                    # btn.setStyleSheet()
                    self.set_widget_background(last_col_widget, grade)
                    print(last_col_widget.styleSheet())
                    continue
                self.table.item(index, i).setBackground(self.getRGBcolor(grade))
                self.table.item(index, i).setTextAlignment(QtCore.Qt.AlignCenter)

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
            return QtGui.QColor(245, 245, 141)

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
        # self.save_button.clicked.connect(self.historyPress)

        self.ok_button.setIcon(QtGui.QIcon('assets/ok.png'))
        self.ok_button.setIconSize(QtCore.QSize(24, 24))
        self.ok_button.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        # self.ok_button.clicked.connect(self.historyPress)

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
    gui = Page2(False)
    # gui.showMaximized()
    gui.show()

    try:
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
        print('closing window...')
