import json
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSizePolicy, QLabel, QPushButton
import publicData as pDt

disunderstand, fuzzy, know = 10, 2, -5  # 权重变化


class OneWord(QWidget):
    def __init__(self, word):
        super(QWidget, self).__init__()
        self.word = word
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        font = QFont()
        font.setPointSize(pDt.settings['pointsize'])
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)

        self.label = QLabel(self)
        size_policy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(size_policy)
        self.label.setFont(font)
        self.label.setTextFormat(Qt.AutoText)
        self.label.setAlignment(Qt.AlignCenter)
        self.horizontalLayout.addWidget(self.label)

        self.pushButton = QPushButton(self)
        size_policy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(size_policy)
        self.pushButton.setFont(font)
        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self)
        size_policy.setHeightForWidth(self.pushButton_2.sizePolicy().hasHeightForWidth())
        self.pushButton_2.setSizePolicy(size_policy)
        self.pushButton_2.setFont(font)
        self.horizontalLayout.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(self)
        size_policy.setHeightForWidth(self.pushButton_3.sizePolicy().hasHeightForWidth())
        self.pushButton_3.setSizePolicy(size_policy)
        self.pushButton_3.setFont(font)
        self.horizontalLayout.addWidget(self.pushButton_3)

        self.pushButton_4 = QPushButton(self)
        size_policy.setHeightForWidth(self.pushButton_4.sizePolicy().hasHeightForWidth())
        self.pushButton_4.setSizePolicy(size_policy)
        self.pushButton_4.setFont(font)
        self.horizontalLayout.addWidget(self.pushButton_4)

        self.pushButton_5 = QPushButton(self)
        size_policy.setHeightForWidth(self.pushButton_5.sizePolicy().hasHeightForWidth())
        self.pushButton_5.setSizePolicy(size_policy)
        self.pushButton_5.setFont(font)
        self.horizontalLayout.addWidget(self.pushButton_5)

        self.label.setText(self.word)
        self.pushButton.setText("查看中文")
        self.pushButton_2.setText("不认识")
        self.pushButton_3.setText("模糊")
        self.pushButton_4.setText("认识")
        self.pushButton_5.setText("完全认识")

        self.pushButton.clicked.connect(self.show_cn)
        self.pushButton_2.clicked.connect(self.btn_disunderstand)
        self.pushButton_3.clicked.connect(self.btn_fuzzy)
        self.pushButton_4.clicked.connect(self.btn_know)
        self.pushButton_5.clicked.connect(self.del_word)

    # 查看中文
    def show_cn(self):
        self.pushButton.setText(pDt.words[self.word][1])
        self.pushButton.setEnabled(False)

    # 不认识
    def btn_disunderstand(self):
        pDt.words[self.word][0] += disunderstand
        pDt.hard_words[self.word] = pDt.streak
        # 更新困难词
        with open('hard_words.json', 'w', encoding='utf-8') as f:
            json.dump(pDt.hard_words, f, ensure_ascii=False)
        self.close()
        del self

    # 模糊
    def btn_fuzzy(self):
        pDt.words[self.word][0] += fuzzy
        pDt.hard_words[self.word] = pDt.streak
        # 更新困难词
        with open('hard_words.json', 'w', encoding='utf-8') as f:
            json.dump(pDt.hard_words, f, ensure_ascii=False)
        self.close()
        del self

    # 认识
    def btn_know(self):
        pDt.words[self.word][0] += know
        if pDt.words[self.word][0] <= 0:
            pDt.words[self.word][0] = 1
        if self.word in pDt.hard_words:
            pDt.hard_words[self.word] -= 1
            if pDt.hard_words[self.word] == 0:
                pDt.hard_words.pop(self.word)
            # 更新困难词
            with open('hard_words.json', 'w', encoding='utf-8') as f:
                json.dump(pDt.hard_words, f, ensure_ascii=False)
        self.close()
        del self

    # 完全认识
    def del_word(self):
        pDt.easy_words[self.word] = pDt.words[self.word][1]
        with open('easy_words.json', 'w', encoding='utf-8') as f:
            json.dump(pDt.easy_words, f, ensure_ascii=False)
        if self.word in pDt.hard_words:
            pDt.hard_words.pop(self.word)
            # 更新困难词
            with open('hard_words.json', 'w', encoding='utf-8') as f:
                json.dump(pDt.hard_words, f, ensure_ascii=False)
        pDt.tp.sw.del_words.append(self.word)
        self.close()
        del self

    def closeEvent(self, event):
        pDt.tp.sw.ow_count -= 1
        if pDt.tp.sw.ow_count == 0:
            pDt.tp.sw.close()
