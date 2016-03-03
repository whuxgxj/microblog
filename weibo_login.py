#-*- coding:utf-8-*-
import re
import locale
import operator
import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import codecs
from ext import *
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class Main(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.initUI()
        mycode = locale.getpreferredencoding()
        code = QTextCodec.codecForName(mycode)
        QTextCodec.setCodecForLocale(code)
        QTextCodec.setCodecForTr(code)
        QTextCodec.setCodecForCStrings(code)

    def initUI(self):
        self.initMenubar()
        self.arraydata = []
        self.table = QTableView()
        self.setCentralWidget(self.table)
        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Main window')
        self.show()

    def initMenubar(self):
        # 文件菜单
        self.openAction = QAction(u"&打开", self)
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.triggered.connect(self.open)

        self.saveAction = QAction(u"&保存", self)
        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.triggered.connect(self.save)

        self.deleteAction = QAction(u"&删除", self)
        self.deleteAction.setShortcut("Ctrl+D")
        self.deleteAction.triggered.connect(self.delete)

        # 编辑菜单
        self.findAction = QAction(u"&查找", self)
        self.findAction.triggered.connect(self.find)

        self.replaceAction = QAction(u"&替换", self)
        self.replaceAction.triggered.connect(self.replace)

        # 运行菜单
        self.singleWAction = QAction(u"&单微博爬取", self)
        self.singleWAction.triggered.connect(self.singleW)

        self.singleUAction = QAction(u"&单用户爬取", self)
        self.singleUAction.triggered.connect(self.singleU)

        self.selfinfoAction = QAction(u"&个人信息爬取", self)
        self.selfinfoAction.triggered.connect(self.selfinfo)

        self.topicAction = QAction(u"&微博话题爬取", self)
        self.topicAction.triggered.connect(self.topic)

        # 设置菜单
        self.colorAction = QAction(u"&颜色", self)
        self.colorAction.triggered.connect(self.color)

        self.fontAction = QAction(u"&字体", self)
        self.fontAction.triggered.connect(self.font)

        self.themeAction = QAction(u"&主题", self)
        self.themeAction.triggered.connect(self.theme)

        self.proxyAction = QAction(u"&代理", self)
        self.proxyAction.triggered.connect(self.proxy)

        self.uaAction = QAction(u"&UA", self)
        self.uaAction.triggered.connect(self.ua)

        # 关于菜单
        self.helpAction = QAction(u"&帮助", self)
        self.helpAction.triggered.connect(self.help)

        self.infoAction = QAction(u"&关于本软件", self)
        self.infoAction.triggered.connect(self.info)

        menubar = self.menuBar()

        file = menubar.addMenu(u"&文件")
        edit = menubar.addMenu(u"&编辑")
        run = menubar.addMenu(u"&运行")
        setting = menubar.addMenu(u"&设置")
        analysis = menubar.addMenu(u"&分析")
        about = menubar.addMenu(u"&关于")

        # Add the most important actions to the menubar

        file.addAction(self.openAction)
        file.addAction(self.saveAction)
        file.addAction(self.deleteAction)

        edit.addAction(self.findAction)
        edit.addAction(self.replaceAction)

        run.addAction(self.singleWAction)
        run.addAction(self.singleUAction)
        run.addAction(self.selfinfoAction)
        run.addAction(self.topicAction)

        setting.addAction(self.colorAction)
        setting.addAction(self.fontAction)
        setting.addAction(self.themeAction)
        setting.addAction(self.proxyAction)
        setting.addAction(self.uaAction)

        about.addAction(self.helpAction)
        about.addAction(self.infoAction)

    def createTable(self):

        # set the table model
        tm = MyTableModel(self.arraydata[1:], self.header, self)
        self.table.setModel(tm)

        # set the minimum size
        self.table.setMinimumSize(400, 300)

        # hide grid
        self.table.setShowGrid(False)

        # set the font
        font = QFont("Courier New", 8)
        self.table.setFont(font)

        # hide vertical header
        vh = self.table.verticalHeader()
        vh.setVisible(False)

        # set horizontal header properties
        hh = self.table.horizontalHeader()
        hh.setStretchLastSection(True)

        # set column width to fit contents
        self.table.resizeColumnsToContents()

        # set row height
        nrows = len(self.arraydata)
        for row in xrange(nrows):
            self.table.setRowHeight(row, 18)

        # enable sorting
        self.table.setSortingEnabled(True)

    def open(self):
        self.arraydata = []
        # Get filename and show only .writer files
        self.filename = QFileDialog.getOpenFileName(self,
                                                    u"选取文件", ".", "All Files (*);;Text Files (*.csv)")  # 设置文件扩展名过滤,注意用双分号间隔
        if str(self.filename).endswith(".txt"):
            with open(self.filename, "rt") as file:
                for line in file.readlines():
                    self.arraydata.append(line.split(' '))
        if str(self.filename).endswith(".csv"):
            import csv
            csvfile = open(self.filename, 'rb')
            reader = csv.reader(csvfile)
            for line in reader:
                l = [li.encode("utf-8").decode("utf-8") for li in line]
                print l
                self.arraydata.append(l)
            csvfile.close()
        self.header = self.arraydata[0]
        self.createTable()

    def save(self):
        pass

    def delete(self):
        pass

    def find(self):
        pass

    def replace(self):
        pass

    def singleW(self):
        su=singleweibo.SingleWeibo(self)
        su.show()

    def singleU(self):
        pass

    def selfinfo(self):
        pass

    def topic(self):
        pass

    def color(self):
        pass

    def font(self):
        pass

    def theme(self):
        pass

    def proxy(self):
        pass

    def ua(self):
        pass

    def help(self):
        lg = login.Login(self)
        lg.show()

    def info(self):
        pass


class MyTableModel(QAbstractTableModel):

    def __init__(self, datain, headerdata, parent=None, *args):
        """ datain: a list of lists
            headerdata: a list of strings
        """
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain
        self.headerdata = headerdata

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.arraydata[0])

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.arraydata[index.row()][index.column()])

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        return QVariant()

    def sort(self, Ncol, order):
        """Sort table by given column number.
        """
        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.arraydata = sorted(self.arraydata, key=operator.itemgetter(Ncol))
        if order == Qt.DescendingOrder:
            self.arraydata.reverse()
        self.emit(SIGNAL("layoutChanged()"))


def main():
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec_())
if __name__ == '__main__':
    main()
