# -*- coding: utf-8 -*-
import json
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSizePolicy, QLabel, QPushButton
import public_data as pdt


class EditWord(QWidget):
    def __init__(self, word):
        super(QWidget, self).__init__()
        self.word = word
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.h1 = QHBoxLayout()
        self.h2 = QHBoxLayout()
        self.w1 = QWidget()
        self.w1.setLayout(self.h1)
        self.w2 = QWidget()
        self.w2.setLayout(self.h2)

        font = QFont()
        font.setPointSize(16)
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)

        self.label_eng = QLabel(self)
        size_policy.setHeightForWidth(self.label_eng.sizePolicy().hasHeightForWidth())
        self.label_eng.setSizePolicy(size_policy)
        self.label_eng.setFont(font)
        self.label_eng.setTextFormat(Qt.AutoText)
        self.label_eng.setAlignment(Qt.AlignCenter)
        self.h1.addWidget(self.label_eng)

        self.label_w = QLabel(self)
        size_policy.setHeightForWidth(self.label_w.sizePolicy().hasHeightForWidth())
        self.label_w.setSizePolicy(size_policy)
        self.label_w.setFont(font)
        self.label_w.setTextFormat(Qt.AutoText)
        self.label_w.setAlignment(Qt.AlignCenter)
        self.h1.addWidget(self.label_w)

        self.label_cn = QLabel(self)
        size_policy.setHeightForWidth(self.label_cn.sizePolicy().hasHeightForWidth())
        self.label_cn.setSizePolicy(size_policy)
        self.label_cn.setFont(font)
        self.label_cn.setTextFormat(Qt.AutoText)
        self.label_cn.setAlignment(Qt.AlignCenter)

        self.btn_edit = QPushButton(self)
        size_policy.setHeightForWidth(self.btn_edit.sizePolicy().hasHeightForWidth())
        self.btn_edit.setSizePolicy(size_policy)
        self.btn_edit.setFont(font)
        self.h2.addWidget(self.btn_edit)

        self.btn_del = QPushButton(self)
        size_policy.setHeightForWidth(self.btn_del.sizePolicy().hasHeightForWidth())
        self.btn_del.setSizePolicy(size_policy)
        self.btn_del.setFont(font)
        self.h2.addWidget(self.btn_del)

        self.horizontalLayout.addWidget(self.w1)
        self.horizontalLayout.addWidget(self.label_cn)
        self.horizontalLayout.addWidget(self.w2)

        self.label_eng.setText(self.word)
        self.label_w.setText(str(pdt.words[self.word][0]))
        self.label_cn.setText(pdt.words[self.word][1])
        self.btn_edit.setText('编辑')
        self.btn_del.setText('删除')

        self.btn_edit.clicked.connect(self.edit_word_window)
        self.btn_del.clicked.connect(self.del_word)

    def edit_word_window(self):
        pdt.word_editing.set_self('编辑单词', self.word, pdt.words[self.word][0], pdt.words[self.word][1])
        pdt.word_editing.show()

    def del_word(self):
        if self.word in pdt.hard_words:
            pdt.hard_words.pop(self.word)
            # 更新困难词
            with open('hard_words.json', 'w', encoding='utf-8') as f:
                json.dump(pdt.hard_words, f, ensure_ascii=False)
        del pdt.words[self.word]
        del pdt.vw.edit_words[self.word]
        self.close()
        del self
