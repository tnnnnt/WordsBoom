from PyQt5.QtCore import QTimer, QThread, QCoreApplication, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
import publicData as pDt
from seSe import SeSe
from showWords import ShowWords
from work import Work


def showWordsFile():
    file_path = "words.csv"
    url = QUrl.fromLocalFile(file_path)
    QDesktopServices.openUrl(url)


class MySystemTrayIcon(QSystemTrayIcon):  # 系统托盘图标类
    def __init__(self):
        super(MySystemTrayIcon, self).__init__()
        self.se = None
        self.sw = None
        self.setIcon(pDt.icon)
        self.setToolTip(
            "单词弹弹弹\n间隔分钟数: " + str(pDt.settings['minute']) + "\n单次单词数: " + str(pDt.settings['number']))

        self.tpMenu = QMenu()
        self.a1 = QAction('启动')
        self.a2 = QAction('设置')
        self.a3 = QAction('编辑词库')

        self.a_exit = QAction('退出')

        self.tpMenu.addAction(self.a1)
        self.tpMenu.addAction(self.a2)
        self.tpMenu.addAction(self.a3)
        self.tpMenu.addAction(self.a_exit)
        self.setContextMenu(self.tpMenu)

        self.a1.triggered.connect(self.startOrStop)
        self.a2.triggered.connect(self.setSet)
        self.a3.triggered.connect(showWordsFile)
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
        self.a1.setEnabled(False)
        self.sw = ShowWords()
        self.sw.exec()

    def leftAct(self, reason):
        # 鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
        if reason == 3:
            self.setSet()
