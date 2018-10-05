# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'HJ_UI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

import sys, winreg
import threading

from PyQt5.QtWidgets import QFileDialog, QApplication, QMainWindow, QWidget, QGridLayout,QSizePolicy,QPushButton,QLineEdit,QMessageBox
from PyQt5.QtCore import QThread,QSize
from PyQt5.QtGui import QFont

from HJ_Excel import DivideProfit


def get_desktop():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')  # 利用系统的链表
    return winreg.QueryValueEx(key, "Desktop")[0]


class BackendThread(QThread):
    # 处理业务逻辑
    def __init__(self, pre_month, ths_month, ths_billing, save_to):
        super(BackendThread, self).__init__()
        self.dp = DivideProfit(pre_month, ths_month, ths_billing, save_to)

    def run(self):
        self.dp.process()


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.show()

    def setupUi(self):
        self.setFixedSize(550, 220)
        self.centralwidget = QWidget(self)
        self.centralwidget.resize(self.width(), self.height())
        self.setWindowTitle('河津分账')
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setContentsMargins(-1, -1, -1, 0)
        self.gridLayout.setHorizontalSpacing(20)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QPushButton('本月')
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setObjectName("btn-1")
        self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 1)
        self.pushButton_2 = QPushButton('上月')
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setObjectName("btn-2")
        self.gridLayout.addWidget(self.pushButton_2, 1, 0, 1, 1)
        self.lineEdit_2 = QLineEdit(self.centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy)
        self.lineEdit_2.setMinimumSize(QSize(300, 0))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.confirm_button = QPushButton('开始')
        self.cancile_button = QPushButton('取消')
        self.gridLayout.addWidget(self.confirm_button, 4, 5, 1, 1)
        self.gridLayout.addWidget(self.cancile_button, 4, 6, 1, 1)

        self.pushButton_3 = QPushButton('本月出账明细')
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setSizeIncrement(QSize(0, 0))
        self.pushButton_3.setBaseSize(QSize(0, 0))
        font = QFont()
        font.setFamily("Agency FB")
        font.setPointSize(8)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("btn-3")
        self.gridLayout.addWidget(self.pushButton_3, 2, 0, 1, 1)
        self.pushButton_4 = QPushButton('保存到...')
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(sizePolicy)
        self.pushButton_4.setObjectName("btn-4")
        self.gridLayout.addWidget(self.pushButton_4, 3, 0, 1, 1)
        self.lineEdit_4 = QLineEdit(self.centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_4.sizePolicy().hasHeightForWidth())
        self.lineEdit_4.setSizePolicy(sizePolicy)
        self.lineEdit_4.setMinimumSize(QSize(300, 0))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout.addWidget(self.lineEdit_4, 3, 1, 1, 1)
        self.lineEdit_3 = QLineEdit(self.centralwidget)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_3.setSizePolicy(sizePolicy)
        self.lineEdit_3.setMinimumSize(QSize(300, 0))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout.addWidget(self.lineEdit_3, 2, 1, 1, 1)
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMinimumSize(QSize(300, 0))
        self.lineEdit.setAutoFillBackground(False)
        self.lineEdit.setFrame(True)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_3.setReadOnly(True)
        self.lineEdit_4.setReadOnly(True)
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.pushButton.clicked.connect(self.showDialog)
        self.pushButton_2.clicked.connect(self.showDialog)
        self.pushButton_3.clicked.connect(self.showDialog)
        self.pushButton_4.clicked.connect(self.showDialog)
        self.confirm_button.clicked.connect(self.accept)
        self.cancile_button.clicked.connect(self.reject)

    def accept(self):
        pre_month = self.lineEdit.text()
        ths_month = self.lineEdit_2.text()
        pre_month_billing = self.lineEdit_3.text()
        save_to = self.lineEdit_4.text()
        if pre_month == '' or ths_month == '' or pre_month_billing == '' or save_to == '':
            QMessageBox.information(self, "错误",
                                              self.tr("请选择路径！"))
            return

        self.setEnabled(False)
        self.back = BackendThread(pre_month, ths_month, pre_month_billing, save_to)
        t1 = threading.Thread(target=self.is_over)
        self.back.start()
        t1.start()

    def is_over(self):
        while True:
            if self.back.isFinished():
                self.setEnabled(True)
                break

    def reject(self):
        qApp = QApplication.instance()
        qApp.quit()

    def showDialog(self):
        sender = self.sender()
        btn_index = sender.objectName().split('-')[-1]
        if btn_index in ['1', '2']:
            path = QFileDialog.getExistingDirectory(directory=get_desktop())
            if btn_index == '1':
                self.lineEdit.setText(path)
            elif btn_index == '2':
                self.lineEdit_2.setText(path)
        elif btn_index == '3':
            path = QFileDialog.getOpenFileName(directory=get_desktop(), filter='*.xls;;*.xlsx')
            self.lineEdit_3.setText(path[0])
        elif btn_index == '4':
            path = QFileDialog.getExistingDirectory(directory=get_desktop())
            self.lineEdit_4.setText(path)


app = QApplication(sys.argv)
ui = Ui_MainWindow()
sys.exit(app.exec_())
