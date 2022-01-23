from fileinput import close
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem,QPushButton
from PyQt5 import uic, QtGui, QtCore

from History import History
from app import MyApp

class Page2(QMainWindow):
    def __init__(self, isReadFileMode):
        super().__init__()
        # print(os.listdir())
        uic.loadUi('./src/page2.ui', self)
        self.setButton()
        self.setTable()
        self.setAlgorithmList()
        self.historyApp = None
        self.MyApp = None

    def setAlgorithmList(self):
        self.list_used_algo.addItems(["first","second"])
        self.list_unused_algo.addItems(["third"])


    def setTable(self):
        width = self.table.frameGeometry().width()
        col0_size = 300
        col2_size = 200
        col1_size = width - (col0_size  + col2_size) - 30
        self.table.setColumnWidth(0,col0_size)
        self.table.setColumnWidth(1,col1_size)
        self.table.setColumnWidth(2,col2_size)
        
        self.addRows()

    def addRows(self):
        rows = [{"organs":"something1","detection":"somewhere1"},
        {"organs":"something2","detection":"somewhere2"},
        {"organs":"something3","detection":"somewhere3"}]


        self.table.setRowCount(len(rows))
        for index,row in enumerate(rows):
            self.table.setItem(index,0, QTableWidgetItem(row["organs"]))
            self.table.setItem(index,1, QTableWidgetItem(row["detection"]))
            btn = QPushButton('')
            btn.setIcon(QtGui.QIcon('./src/assets/eye.png'))
            btn.setIconSize(QtCore.QSize(12, 12))
            btn.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
            self.table.setCellWidget(index,2,btn)
            for i in range(0,3):
                if i == 2 :
                    btn.setStyleSheet(self.getBackgroundColortext(index))
                    continue
                self.table.item(index, i).setBackground(self.getRGBcolor(index))
                self.table.item(index, i).setTextAlignment(QtCore.Qt.AlignCenter )
            
            
            

    def getRGBcolor(self,colorNumber):
        #colorNmber -> 1 :red , 2 :green , else:yellow
        if(colorNumber == 1):
            return QtGui.QColor(245, 141, 141)
        elif(colorNumber == 2):
            return QtGui.QColor(141, 245, 193)
        else:
            return QtGui.QColor(245, 245, 141)

    def getBackgroundColortext(self,colorNumber):
        #colorNmber -> 1 :red , 2 :green , else:yellow
        if(colorNumber == 1):
            return "background-color: rgba(245, 141, 141);"
        elif(colorNumber == 2):
            return "background-color: rgba(141, 245, 193);"
        else:
            return "background-color: rgba(245, 245, 141);"


    def setButton(self):
        self.home_button.setIcon(QtGui.QIcon('./src/assets/home.png'))
        self.home_button.setIconSize(QtCore.QSize(24, 24))
        self.home_button.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.home_button.clicked.connect(self.homePress)

        self.history_button.setIcon(QtGui.QIcon('./src/assets/history.png'))
        self.history_button.setIconSize(QtCore.QSize(24, 24))
        self.history_button.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.history_button.clicked.connect(self.historyPress)

        self.exit_button.setIcon(QtGui.QIcon('./src/assets/log-out.png'))
        self.exit_button.setIconSize(QtCore.QSize(24, 24))
        self.exit_button.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        self.exit_button.clicked.connect(self.close)


        self.save_button.setIcon(QtGui.QIcon('./src/assets/save.png'))
        self.save_button.setIconSize(QtCore.QSize(24, 24))
        self.save_button.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        #self.save_button.clicked.connect(self.historyPress)

        

        self.ok_button.setIcon(QtGui.QIcon('./src/assets/ok.png'))
        self.ok_button.setIconSize(QtCore.QSize(24, 24))
        self.ok_button.setStyleSheet("background-color: rgba(255, 255, 255, 0);")
        #self.ok_button.clicked.connect(self.historyPress)

    def historyPress(self):
        if self.historyApp == None:
            self.historyApp = History()
        self.historyApp.show()
        self.close()
    
    def homePress(self):
        if self.MyApp == None:
            self.MyApp = MyApp(False)
        self.MyApp.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = Page2(False)
    gui.show()

    try:
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
        print('closing window...')
