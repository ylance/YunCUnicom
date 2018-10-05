import sys,datetime
from PyQt5.QtWidgets import QWidget, QLabel, QApplication,QDesktopWidget,QLineEdit,QFormLayout,QCalendarWidget,QPushButton,QHBoxLayout,QMessageBox,QTextEdit
from PyQt5.QtCore import Qt, QDate, QRegExp, QThread
from PyQt5 import QtCore
from PyQt5.QtGui import QRegExpValidator,QTextCursor
from AutoCheck import AutoCheck
import threading


class BackendThread(QThread):
    # 处理业务逻辑

    def __init__(self, username, password, date, page_no):
        super(BackendThread,self).__init__()
        self.username = username
        self.password = password
        self.date = date
        self.page_no = page_no
        # self.t = Test()
        self.auto = AutoCheck(self.username, self.password, self.date, self.page_no)

    def run(self):
        # self.auto.main()
        # self.t.main()
        main_thread = threading.Thread(target=self.auto.main)
        deamon_thread = threading.Thread(target=self.auto.deamon)
        main_thread.setDaemon(True)
        main_thread.start()
        deamon_thread.start()


class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

    def flush(self):
        self.buff = ''


# QButtonGroup 还没弄明白如何使用， 暂时使用 QHBoxLayout 中添加两个按钮。
class Double_I(QWidget):
    def __init__(self):
        super(Double_I,self).__init__()
        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
        # sys.stder = EmittingStream(textWritten=self.normalOutputWritten)

        self.main_layout = QHBoxLayout()
        self.left_layout = QFormLayout()
        self.right_layout = QFormLayout()
        self.button_layout = QHBoxLayout()

        self.label_username = QLabel('用户名:')
        self.label_password = QLabel('密码:')
        self.label_date = QLabel('日期:')
        self.label_page = QLabel('页码:')
        self.hide_date = QLabel()

        self.user_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.page_edit = QLineEdit()
        self.text_edit = QTextEdit()
        self.cal = QCalendarWidget()
        self.confirm_button = QPushButton('开始')
        self.cancile_button = QPushButton('取消')

        # self.buttons = QButtonGroup()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("实名制抽检")
        self.resize(600,330)
        self.set_label()
        self.center()
        self.setFixedSize(self.width(), self.height())
        self.show()

    def center(self):
        win = self.frameGeometry()
        center_pointer = QDesktopWidget().availableGeometry().center()
        win.moveCenter(center_pointer)
        self.move(win.topLeft())

    def showDate(self, date):
        pydate = date.toPyDate()
        show_date = datetime.datetime.strftime(pydate,"%Y-%m-%d")
        self.hide_date.setText(show_date)

    def close_app(self):
        try:
            # self.back.auto.quit_app()
            self.back.auto.stop = True
            self.confirm_button.setEnabled(True)
            self.back.quit()
            self.back.wait()

        except Exception as e:
            pass

    def set_label(self):
        page_validator = QRegExpValidator()
        self.confirm_button.clicked.connect(self.confirm_clicked)
        self.cancile_button.clicked.connect(self.close_app)
        self.button_layout.addStretch(1)
        self.button_layout.addWidget(self.confirm_button)
        self.button_layout.addWidget(self.cancile_button)

        reg = QRegExp(r'[1-9]|[1-9]\d|1\d\d|200')
        page_validator.setRegExp(reg)

        self.user_edit.setMaximumWidth(200)
        self.user_edit.setText("SXYC0037")
        self.password_edit.setMaximumWidth(200)
        self.password_edit.setEchoMode(2)
        self.password_edit.setText('jiahuan123+')
        self.page_edit.setMaximumWidth(30)
        self.page_edit.setMaxLength(3)
        self.page_edit.setText('1')
        self.page_edit.setAlignment(Qt.AlignRight)
        self.page_edit.setValidator(page_validator)
        self.cal.setMaximumWidth(200)
        self.hide_date.setHidden(True)
        self.text_edit.setFixedHeight(280)
        self.text_edit.setFixedWidth(325)
        self.text_edit.setReadOnly(True)
        self.text_edit.lineWrapMode()
        self.hide_date.setText(datetime.date.today().strftime("%Y-%m-%d"))

        self.cal.setGridVisible(True)
        self.cal.clicked[QDate].connect(self.showDate)

        self.left_layout.addRow(self.label_username, self.user_edit)
        self.left_layout.addRow(self.label_password, self.password_edit)
        self.left_layout.addRow(self.label_date, self.cal)
        self.left_layout.addRow(self.label_page, self.page_edit)
        self.left_layout.addRow(self.hide_date)
        self.right_layout.addWidget(self.text_edit)
        self.right_layout.addRow(self.button_layout)

        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)
        self.setLayout(self.main_layout)

    def normalOutputWritten(self, text):
        """Append text to the QTextEdit."""
        # Maybe QTextEdit.append() works as well, but this is how I do it:
        cursor = self.text_edit.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.text_edit.setTextCursor(cursor)
        self.text_edit.ensureCursorVisible()

    def confirm_clicked(self):
        username = self.user_edit.text()
        password = self.password_edit.text()
        date = self.hide_date.text()
        page_no = self.page_edit.text()
        reply = QMessageBox.question(self,'提示', '确定抽检'+' '+date+',从第'+page_no+'页开始的订单？', QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                self.confirm_button.setEnabled(False)
                self.back = BackendThread(username,password,date,page_no)
                self.back.start()
                # print('kaishi')
            except Exception as e:
                print('结束')
                print(e)
        else:
            sys.exit(0)


app = QApplication(sys.argv)
double = Double_I()
sys.exit(app.exec_())
