# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from report_data import *
from report_gen import *

class FirstWindow(QWidget):

    def __init__(self, parent=None):
        super(FirstWindow, self).__init__(parent)
        
        self.yearComboBox = QComboBox()
        self.yearComboBox.addItem("2018")
        
        self.monthComboBox = QComboBox()
        for i in range(1, 13):
            self.monthComboBox.addItem(str(i))
        
        self.dayComboBox = QComboBox()
        self.dayComboBox.addItem("")
        for i in range(1, 32):
            self.dayComboBox.addItem(str(i))
        
        btn = QPushButton()
        btn.setText("Generate Report")
        btn.clicked.connect(self.btn_gen_report_clicked)
        
        self.grid = QGridLayout(self)
        self.grid.addWidget(self.yearComboBox, 1, 1)
        self.grid.addWidget(self.monthComboBox, 1, 2)
        self.grid.addWidget(self.dayComboBox, 1, 3)
        self.grid.addWidget(btn, 1, 4)

    def btn_gen_report_clicked(self):
        print("btn_gen_report_clicked.year:" + self.yearComboBox.currentText())
        print("btn_gen_report_clicked.month:" + self.monthComboBox.currentText())
        print("btn_gen_report_clicked.day:" + self.dayComboBox.currentText())
        getReportData(self.yearComboBox.currentText(), self.monthComboBox.currentText(), self.dayComboBox.currentText())
        gen_report()


if __name__ == "__main__":
    App = QApplication(sys.argv)
    ex = FirstWindow()
    ex.show()
    sys.exit(App.exec_())