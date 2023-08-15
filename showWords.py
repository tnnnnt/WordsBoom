import json
import random
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QScrollArea, QWidget
import publicData
from oneWord import OneWord


class ShowWords(QDialog):
    def __init__(self):
        super(QDialog, self).__init__()
        self.setWindowIcon(publicData.icon)
        self.setWindowTitle("单词弹弹弹")
        self.resize(publicData.settings['width'], publicData.settings['height'])
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

        with open('hard_words.json', encoding='UTF-8') as f:
            hard_words = json.load(f)
        count = publicData.settings['number'] - len(hard_words)
        if count >= 0:
            for word in hard_words:
                self.verticalLayout_2.addWidget(OneWord(word))
            words_en, words_w = [], []
            for word in publicData.words:
                if word in hard_words:
                    continue
                words_en.append(word)
                words_w.append(publicData.words[word][0])
            for word in random.choices(words_en, weights=words_w, k=min(count, len(words_en))):
                self.verticalLayout_2.addWidget(OneWord(word))
            self.ow_count = len(hard_words) + min(count, len(words_en))
        else:
            for i in range(publicData.settings['number']):
                self.verticalLayout_2.addWidget(OneWord(hard_words[i]))
            self.ow_count = publicData.settings['number']
        self.hard_words, self.del_words = [], []
        self.setWindowModality(Qt.ApplicationModal)  # 设置为应用程序级别的模态对话框
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # 始终在前面

    def closeEvent(self, event):
        # 窗口关闭时被调用
        # 销毁OneWord子对象
        for child in self.children():
            if isinstance(child, OneWord):
                child.deleteLater()
        # 保存窗口长宽高
        publicData.settings['width'] = self.width()
        publicData.settings['height'] = self.height()
        with open('settings.json', 'w', encoding='utf-8') as f:
            json.dump(publicData.settings, f, ensure_ascii=False)
        # 更新困难词
        with open('hard_words.json', 'w', encoding='utf-8') as f:
            json.dump(self.hard_words, f, ensure_ascii=False)
        # 更新词库
        for word in self.del_words:
            if word in publicData.words:
                del publicData.words[word]
        with open('words.json', 'w', encoding='utf-8') as f:
            json.dump(publicData.words, f, ensure_ascii=False)

        publicData.tp.a1.setEnabled(True)
        # 继续计时
        publicData.tp.timer.start(publicData.settings['minute'] * publicData.ttt)
