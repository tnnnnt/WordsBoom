import csv
import json
import random
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QScrollArea, QWidget, QApplication
import public_data as pdt
from one_word import OneWord


class ShowWords(QDialog):
    def __init__(self):
        super(QDialog, self).__init__()
        self.setWindowIcon(pdt.icon)
        self.setWindowTitle("单词弹弹弹")
        self.resize(pdt.settings['width'], pdt.settings['height'])
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

        count = pdt.settings['number'] - len(pdt.hard_words)
        if count >= 0:
            for word in pdt.hard_words:
                self.verticalLayout_2.addWidget(OneWord(word))
            words_en, words_w = [], []
            for word in pdt.words:
                if word in pdt.hard_words:
                    continue
                words_en.append(word)
                words_w.append(pdt.words[word][0])
            for word in random.choices(words_en, weights=words_w, k=min(count, len(words_en))):
                self.verticalLayout_2.addWidget(OneWord(word))
            self.ow_count = len(pdt.hard_words) + min(count, len(words_en))
        else:
            for i in range(pdt.settings['number']):
                self.verticalLayout_2.addWidget(OneWord(list(pdt.hard_words.keys())[i]))
            self.ow_count = pdt.settings['number']
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
        pdt.settings['width'] = self.width()
        pdt.settings['height'] = self.height()
        with open('settings.json', 'w', encoding='utf-8') as f:
            json.dump(pdt.settings, f, ensure_ascii=False)
        # 更新词库
        for word in self.del_words:
            if word in pdt.words:
                del pdt.words[word]
        with open('words.csv', 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['英文', '权重', '中文']
            csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
            # 写入CSV文件的标题行
            csv_writer.writeheader()
            # 写入数据行
            for english, (weight, chinese) in pdt.words.items():
                csv_writer.writerow({'英文': english, '权重': weight, '中文': chinese})
        pdt.tp.setToolTip("单词弹弹弹\n间隔分钟数: " + str(pdt.settings['minute']) + "\n单次单词数: " + str(
            pdt.settings['number']) + "\n剩余单词数: " + str(len(pdt.words)))

        pdt.tp.a1.setEnabled(True)
        # 继续计时
        pdt.tp.timer.start(pdt.settings['minute'] * pdt.ttt)
