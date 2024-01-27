# coding:utf-8
import json
import sys
import os
import csv
import msvcrt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
import public_data as pdt
from word_editing import WordEditing
from viewer_window import ViewerWindow
from my_system_tray_icon import MySystemTrayIcon


# 文件锁
def checkSingleProcess():
    global PIDFILE
    try:
        PIDFILE = open(os.path.realpath(sys.argv[0]), "r")  # 获取运行的文件路径
        msvcrt.locking(PIDFILE.fileno(), msvcrt.LK_NBLCK, 1)  # 尝试以非阻塞方式锁定文件
    except IOError:
        # 如果文件已被锁定，表示程序已在运行
        # print("相同程序正在运行")
        return False
    return True


if __name__ == '__main__':
    PIDFILE = None  # 初始化 PIDFILE
    # 防止多开
    if not checkSingleProcess():
        sys.exit(-1)

    # 从 CSV 文件中读取单词数据并存储到全局变量中
    with open('words.csv', 'r', newline='', encoding='utf-8') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            english = row['英文']
            weight = int(row['权重'])  # 将权重转换为整数
            chinese = row['中文']
            pdt.words[english] = [weight, chinese]

    # 从 JSON 文件中读取设置信息并存储到全局变量中
    with open('settings.json', encoding='UTF-8') as f:
        pdt.settings = json.load(f)

    # 从 JSON 文件中读取简单单词信息并存储到全局变量中
    with open('easy_words.json', encoding='UTF-8') as f:
        pdt.easy_words = json.load(f)

    # 从 JSON 文件中读取困难单词信息并存储到全局变量中
    with open('hard_words.json', encoding='utf-8') as f:
        pdt.hard_words = json.load(f)

    # 初始化应用程序
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # 窗口关闭时不退出应用程序
    pdt.icon = QIcon('img/icon.png')

    # 初始化单词编辑器和单词查看器窗口
    pdt.word_editing = WordEditing()
    pdt.vw = ViewerWindow()

    # 初始化系统托盘图标
    pdt.tp = MySystemTrayIcon()
    pdt.tp.set_set()  # 设置系统托盘图标
    pdt.tp.showMessage('单词弹弹弹', '欢迎使用单词弹弹弹！', pdt.icon)  # 显示欢迎消息
    pdt.tp.show()  # 显示系统托盘图标
    sys.exit(app.exec_())  # 运行应用程序并进入事件循环
