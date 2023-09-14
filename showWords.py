import csv
import json
import random
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QScrollArea, QWidget, QApplication
import publicData as pDt
from oneWord import OneWord


class ShowWords(QDialog):
    def __init__(self):
        super(QDialog, self).__init__()
        self.setWindowIcon(pDt.icon)
        self.setWindowTitle("单词弹弹弹")
        self.resize(pDt.settings['width'], pDt.settings['height'])
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(Qt.AlignCenter)
        self.verticalLayout_2 = QVBoxLayout()
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setLayout(self.verticalLayout_2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.setLayout(self.verticalLayout)

        count = pDt.settings['number'] - len(pDt.hard_words)
        if count >= 0:
            for word in pDt.hard_words:
                self.verticalLayout_2.addWidget(OneWord(word))
            words_en, words_w = [], []
            for word in pDt.words:
                if word in pDt.hard_words:
                    continue
                words_en.append(word)
                words_w.append(pDt.words[word][0])
            for word in random.choices(words_en, weights=words_w, k=min(count, len(words_en))):
                self.verticalLayout_2.addWidget(OneWord(word))
            self.ow_count = len(pDt.hard_words) + min(count, len(words_en))
        else:
            for i in range(pDt.settings['number']):
                self.verticalLayout_2.addWidget(OneWord(pDt.hard_words[i]))
            self.ow_count = pDt.settings['number']
        self.del_words = []
        self.setWindowModality(Qt.ApplicationModal)  # 设置为应用程序级别的模态对话框
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # 始终在前面
        QApplication.beep()  # 系统提示音

    def closeEvent(self, event):
        # 窗口关闭时被调用
        # 销毁OneWord子对象
        for child in self.children():
            if isinstance(child, OneWord):
                child.deleteLater()
        # 保存窗口长宽高
        pDt.settings['width'] = self.width()
        pDt.settings['height'] = self.height()
        with open('settings.json', 'w', encoding='utf-8') as f:
            json.dump(pDt.settings, f, ensure_ascii=False)
        # 更新词库
        for word in self.del_words:
            if word in pDt.words:
                del pDt.words[word]
        with open('words.csv', 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['英文', '权重', '中文']
            csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
            # 写入CSV文件的标题行
            csv_writer.writeheader()
            # 写入数据行
            for english, (weight, chinese) in pDt.words.items():
                csv_writer.writerow({'英文': english, '权重': weight, '中文': chinese})

        pDt.tp.a1.setEnabled(True)
        # 继续计时
        pDt.tp.timer.start(pDt.settings['minute'] * pDt.ttt)
