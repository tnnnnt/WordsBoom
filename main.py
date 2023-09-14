import json
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
import public_data as pDt
from my_system_tray_icon import MySystemTrayIcon
import csv

if __name__ == '__main__':
    with open('words.csv', 'r', newline='', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            english = row['英文']
            weight = int(row['权重'])  # 将权重转换为整数
            chinese = row['中文']
            pDt.words[english] = [weight, chinese]
    with open('settings.json', encoding='UTF-8') as f:
        pDt.settings = json.load(f)
    with open('easy_words.json', encoding='UTF-8') as f:
        pDt.easy_words = json.load(f)
    with open('hard_words.json', encoding='utf-8') as f:
        pDt.hard_words = json.load(f)
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    pDt.icon = QIcon('img/icon.png')
    pDt.tp = MySystemTrayIcon()
    pDt.tp.show()
    pDt.tp.showMessage('单词弹弹弹', '欢迎使用单词弹弹弹！', pDt.icon)
    sys.exit(app.exec_())
