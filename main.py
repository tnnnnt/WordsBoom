import json
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
import publicData
from mySystemTrayIcon import MySystemTrayIcon

if __name__ == '__main__':
    with open('words.json', encoding='UTF-8') as f_obj:
        publicData.words = json.load(f_obj)
    with open('settings.json', encoding='UTF-8') as f_obj:
        publicData.settings = json.load(f_obj)
    with open('easy_words.json', encoding='UTF-8') as f_obj:
        publicData.easy_words = json.load(f_obj)
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    publicData.icon = QIcon('img/icon.png')
    publicData.tp = MySystemTrayIcon()
    publicData.tp.show()
    publicData.tp.showMessage('单词弹弹弹', '欢迎使用单词弹弹弹！', publicData.icon)
    sys.exit(app.exec_())
