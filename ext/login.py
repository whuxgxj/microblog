#-*- coding:utf-8-*-
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class Login(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.username = QLabel(u"用户名", self)
        self.un_input = QLineEdit()

        self.password = QLabel(u"密码", self)
        self.pw_input = QLineEdit()

        self.check_save = QCheckBox(u"保存密码", self)

        self.sign_in = QPushButton(u"登陆", self)
        self.sign_in.clicked.connect(self.denglu)

        self.sign_up = QPushButton(u"注册", self)
        self.sign_up.clicked.connect(self.register)

        layout = QGridLayout()

        layout.addWidget(self.username, 0, 0)
        layout.addWidget(self.un_input, 0, 1)
        layout.addWidget(self.password, 1, 0)
        layout.addWidget(self.pw_input, 1, 1)
        layout.addWidget(self.check_save, 2, 0)
        layout.addWidget(self.sign_in, 3, 0)
        layout.addWidget(self.sign_up, 3, 1)

        self.setLayout(layout)
        self.setWindowTitle(u"登陆")

    def denglu(self):
        pass

    def register(self):
        pass

