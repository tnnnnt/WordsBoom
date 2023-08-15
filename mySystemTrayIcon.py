from PyQt5.QtCore import QTimer, QThread, QCoreApplication, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
import publicData
from seSe import SeSe
from showWords import ShowWords
from work import Work


def showEasyFile():
    file_path = "easy_words.json"  # 将文件路径替换为你想要打开的特定文件
    url = QUrl.fromLocalFile(file_path)
    QDesktopServices.openUrl(url)


def showHardFile():
    file_path = "hard_words.json"
    url = QUrl.fromLocalFile(file_path)
    QDesktopServices.openUrl(url)


def showWordsFile():
    file_path = "words.json"
    url = QUrl.fromLocalFile(file_path)
    QDesktopServices.openUrl(url)


class MySystemTrayIcon(QSystemTrayIcon):  # 系统托盘图标类
    def __init__(self):
        super(MySystemTrayIcon, self).__init__()
        self.se = None
        self.sw = None
        self.setIcon(publicData.icon)
        self.setToolTip(
            "单词弹弹弹\n间隔分钟数: " + str(publicData.settings['minute']) + "\n单次单词数: " + str(publicData.settings['number']))

        self.tpMenu = QMenu()
        self.a1 = QAction('启动')
        self.a2 = QAction('设置')

        self.a3 = QMenu("打开json文件")
        self.a3_1 = QAction("easy_words.json")
        self.a3_2 = QAction("hard_words.json")
        self.a3_3 = QAction("words.json")
        self.a3.addAction(self.a3_1)
        self.a3.addAction(self.a3_2)
        self.a3.addAction(self.a3_3)

        self.a_exit = QAction('退出')

        self.tpMenu.addAction(self.a1)
        self.tpMenu.addAction(self.a2)
        self.tpMenu.addMenu(self.a3)
        self.tpMenu.addAction(self.a_exit)
        self.setContextMenu(self.tpMenu)

        self.a1.triggered.connect(self.startOrStop)
        self.a2.triggered.connect(self.setSet)
        self.a3_1.triggered.connect(showEasyFile)
        self.a3_2.triggered.connect(showHardFile)
        self.a3_3.triggered.connect(showWordsFile)

        self.a_exit.triggered.connect(self.quitApp)

        # 线程控制
        self.timer = QTimer()
        self.thread = QThread()
        self.work = Work()
        self.work.moveToThread(self.thread)
        self.timer.timeout.connect(self.work.doWork)
        self.work.signal.connect(self.select)
        self.work.signal.connect(self.timer.stop)
        self.activated.connect(self.leftAct)

    def startOrStop(self):
        if self.a1.text() == '启动':
            self.a1.setText('暂停')
            self.thread.start()
            self.select()
        else:
            self.a1.setText('启动')
            self.timer.stop()
            self.thread.quit()
            self.thread.wait()

    def setSet(self):
        self.a2.setEnabled(False)
        self.se = SeSe()
        self.se.show()

    def quitApp(self):
        # 关闭窗体程序
        self.setVisible(False)
        QCoreApplication.instance().quit()

    def select(self):
        self.sw = ShowWords()
        self.a1.setEnabled(False)
        self.sw.exec()

    def leftAct(self, reason):
        # 鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
        if reason == 3:
            self.setSet()