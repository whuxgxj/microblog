#-*- coding:utf-8-*-
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class SingleWeibo(QDialog):

    def __init__(self, parent=None):
		QDialog.__init__(self, parent)
		self.parent = parent
		self.initUI()

    def initUI(self):
        self.sleep_time_lbl = QLabel(u"间隔时间", self)
        self.sleep_time_spinbox = QSpinBox()
        self.sleep_time_spinbox.setMinimum(0)
        self.sleep_time_spinbox.setMaximum(10)
        self.sleep_time_spinbox.setSingleStep(1)

        self.load_time_lbl = QLabel(u"加载时间", self)
        self.load_time_spinbox = QSpinBox()
        self.load_time_spinbox.setMinimum(0)
        self.load_time_spinbox.setMaximum(10)
        self.load_time_spinbox.setSingleStep(1)

        self.input_type = QRadioButton(u"手动输入", self)
        self.input_type2 = QRadioButton(u"输入文件", self)

        self.urllist_lbl = QLabel(u"url列表", self)
        self.urllist_qline = QLineEdit()
        self.urllist_choose_button = QPushButton(u"选择", self)
        self.urllist_choose_button.clicked.connect(self.choose_file)

        self.ouput_lbl = QLabel(u"输出地址", self)
        self.ouput_qline = QLineEdit()
        self.ouput_choose_button = QPushButton(u"选择", self)
        self.ouput_choose_button.clicked.connect(self.choose_file)

        self.run_singleu = QPushButton(u"运行", self)
        self.run_singleu.clicked.connect(self.singlew)

        layout = QGridLayout()

        layout.addWidget(self.sleep_time_lbl, 0, 0)
        layout.addWidget(self.sleep_time_spinbox, 0, 1)
        layout.addWidget(self.load_time_lbl, 0, 2)
        layout.addWidget(self.load_time_spinbox, 0, 3)
        layout.addWidget(self.input_type, 1, 0, 1, 2)
        layout.addWidget(self.input_type2, 1, 2, 1, 2)
        layout.addWidget(self.urllist_lbl, 2, 0)
        layout.addWidget(self.urllist_qline, 2, 1)
        layout.addWidget(self.urllist_choose_button, 2, 2)
        layout.addWidget(self.ouput_lbl, 3, 0)
        layout.addWidget(self.ouput_qline, 3, 1)
        layout.addWidget(self.ouput_choose_button, 3, 2)
        layout.addWidget(self.run_singleu, 4, 0)
        self.setLayout(layout)
        self.setWindowTitle(u"单微博抓取")

    def singlew(self):
        sleep_time=self.sleep_time_spinbox.value()
        load_time=self.load_time_spinbox.value()
        if self.input_type.isChecked():
            pass

        #if self.input_type2.clicked

    def choose_file(self):
        pass
