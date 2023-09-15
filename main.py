import json
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
import public_data as pdt
from my_system_tray_icon import MySystemTrayIcon
import csv


def on_exit():
    # 在这个槽函数中执行你想要的操作
    with open('run.txt', 'w', encoding='utf-8') as f:
        f.write('0')  # 将程序运行标记重置为0


if __name__ == '__main__':
    # 从文件加载当前库存信息
    with open('run.txt', 'r', encoding='utf-8') as f:
        if f.read() == '1':
            sys.exit()
    with open('run.txt', 'w', encoding='utf-8') as f:
        f.write('1')
    with open('words.csv', 'r', newline='', encoding='utf-8') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            english = row['英文']
            weight = int(row['权重'])  # 将权重转换为整数
            chinese = row['中文']
            pdt.words[english] = [weight, chinese]
    with open('settings.json', encoding='UTF-8') as f:
        pdt.settings = json.load(f)
    with open('easy_words.json', encoding='UTF-8') as f:
        pdt.easy_words = json.load(f)
    with open('hard_words.json', encoding='utf-8') as f:
        pdt.hard_words = json.load(f)
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    pdt.icon = QIcon('img/icon.png')
    pdt.tp = MySystemTrayIcon()
    pdt.tp.show()
    pdt.tp.showMessage('单词弹弹弹', '欢迎使用单词弹弹弹！', pdt.icon)
    app.aboutToQuit.connect(on_exit)
    sys.exit(app.exec_())
