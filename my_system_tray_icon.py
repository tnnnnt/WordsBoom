from PyQt5.QtCore import QTimer, QThread, QCoreApplication, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
import public_data as pDt
from se_se import SeSe
from show_words import ShowWords
from work import Work


def show_words_file():
    file_path = "words.csv"
    url = QUrl.fromLocalFile(file_path)
    QDesktopServices.openUrl(url)


class MySystemTrayIcon(QSystemTrayIcon):  # 系统托盘图标类
    def __init__(self):
        super(MySystemTrayIcon, self).__init__()
        self.se = None
        self.sw = None
        self.setIcon(pDt.icon)
        self.setToolTip("单词弹弹弹\n间隔分钟数: " + str(pDt.settings['minute']) + "\n单次单词数: " + str(
            pDt.settings['number']) + "\n剩余单词数: " + str(len(pDt.words)))

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

        self.a1.triggered.connect(self.start_or_stop)
        self.a2.triggered.connect(self.set_set)
        self.a3.triggered.connect(show_words_file)
        self.a_exit.triggered.connect(self.quit_app)

        # 线程控制
        self.timer = QTimer()
        self.thread = QThread()
        self.work = Work()
        self.work.moveToThread(self.thread)
        self.timer.timeout.connect(self.work.do_work)
        self.work.signal.connect(self.select)
        self.work.signal.connect(self.timer.stop)
        self.activated.connect(self.left_act)

    def start_or_stop(self):
        if self.a1.text() == '启动':
            self.a1.setText('暂停')
            self.thread.start()
            self.select()
        else:
            self.a1.setText('启动')
            self.timer.stop()
            self.thread.quit()
            self.thread.wait()

    def set_set(self):
        self.a2.setEnabled(False)
        self.se = SeSe()
        self.se.show()

    def quit_app(self):
        # 关闭窗体程序
        self.setVisible(False)
        QCoreApplication.instance().quit()

    def select(self):
        self.a1.setEnabled(False)
        self.sw = ShowWords()
        self.sw.exec()

    def left_act(self, reason):
        # 鼠标点击icon传递的信号会带有一个整形的值，1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
        if reason == 3:
            self.set_set()
