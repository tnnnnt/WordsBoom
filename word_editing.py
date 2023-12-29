# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSizePolicy, QLabel, QPushButton, \
    QMessageBox, QVBoxLayout, QDialog, QPlainTextEdit, QSpinBox, QLineEdit
import public_data as pdt
from edit_word import EditWord


class WordEditing(QDialog):
    def __init__(self):
        super(QDialog, self).__init__()
        self.title = None
        self.eng = None
        self.w = None
        self.cn = None
        self.setWindowIcon(pdt.icon)
        self.setFixedSize(240, 300)
        self.v = QVBoxLayout(self)
        self.v.setSpacing(0)
        self.v.setContentsMargins(0, 0, 0, 0)
        self.h1 = QHBoxLayout()
        self.h2 = QHBoxLayout()
        self.h3 = QHBoxLayout()
        self.h4 = QHBoxLayout()
        self.w1 = QWidget()
        self.w1.setLayout(self.h1)
        self.v.addWidget(self.w1)
        self.w2 = QWidget()
        self.w2.setLayout(self.h2)
        self.v.addWidget(self.w2)
        self.w3 = QWidget()
        self.w3.setLayout(self.h3)
        self.v.addWidget(self.w3)
        self.w4 = QWidget()
        self.w4.setLayout(self.h4)
        self.v.addWidget(self.w4)

        font = QFont()
        font.setPointSize(16)
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)

        self.label_eng = QLabel()
        size_policy.setHeightForWidth(self.label_eng.sizePolicy().hasHeightForWidth())
        self.label_eng.setSizePolicy(size_policy)
        self.label_eng.setFont(font)
        self.label_eng.setTextFormat(Qt.AutoText)
        self.label_eng.setAlignment(Qt.AlignCenter)
        self.label_eng.setText('英文')
        self.h1.addWidget(self.label_eng)

        self.label_w = QLabel()
        size_policy.setHeightForWidth(self.label_w.sizePolicy().hasHeightForWidth())
        self.label_w.setSizePolicy(size_policy)
        self.label_w.setFont(font)
        self.label_w.setTextFormat(Qt.AutoText)
        self.label_w.setAlignment(Qt.AlignCenter)
        self.label_w.setText('权重')
        self.label_w.setAlignment(Qt.AlignLeft)
        self.h2.addWidget(self.label_w)

        self.label_cn = QLabel()
        size_policy.setHeightForWidth(self.label_cn.sizePolicy().hasHeightForWidth())
        self.label_cn.setSizePolicy(size_policy)
        self.label_cn.setFont(font)
        self.label_cn.setTextFormat(Qt.AutoText)
        self.label_cn.setAlignment(Qt.AlignCenter)
        self.label_cn.setText('中文')
        self.h3.addWidget(self.label_cn)

        self.le_eng = QLineEdit()
        self.le_eng.setFont(font)
        self.sb_w = QSpinBox()
        self.sb_w.setMaximum(10000)
        self.sb_w.setMinimum(1)
        self.pte_cn = QPlainTextEdit()
        self.pte_cn.setFont(font)
        self.h1.addWidget(self.le_eng)
        self.h2.addWidget(self.sb_w)
        self.h3.addWidget(self.pte_cn)

        self.btn_sure = QPushButton()
        self.btn_sure.setText('确定')
        self.btn_cancel = QPushButton()
        self.btn_cancel.setText('取消')
        self.h4.addWidget(self.btn_sure)
        self.h4.addWidget(self.btn_cancel)

        self.btn_sure.clicked.connect(self.sure_event)
        self.btn_cancel.clicked.connect(self.close)

        self.setWindowModality(Qt.ApplicationModal)  # 设置为应用程序级别的模态对话框
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)  # 始终在前面

    def sure_event(self):
        new_eng = self.le_eng.text()
        new_w = self.sb_w.value()
        new_cn = self.pte_cn.toPlainText()
        if new_eng == '' or new_cn == '':
            QMessageBox.critical(self, '错误', '英文和中文不能为空！')
        elif new_eng != self.eng and (new_eng in pdt.easy_words or new_eng in pdt.words):
            QMessageBox.critical(self, '错误', '该单词已在词库中！')
        elif self.eng == '':  # 新建单词
            pdt.words[new_eng] = [new_w, new_cn]
            pdt.vw.edit_words[new_eng] = EditWord(new_eng)
            pdt.vw.verticalLayout_2.addWidget(pdt.vw.edit_words[new_eng])
            self.close()
        else:  # 编辑单词
            pdt.vw.edit_words[self.eng].del_word()
            pdt.words[new_eng] = [new_w, new_cn]
            pdt.vw.edit_words[new_eng] = EditWord(new_eng)
            pdt.vw.verticalLayout_2.addWidget(pdt.vw.edit_words[new_eng])
            self.close()

    def set_self(self, title, eng, w, cn):
        self.title = title
        self.eng = eng
        self.w = w
        self.cn = cn
        self.setWindowTitle(self.title)
        self.le_eng.setText(self.eng)
        self.sb_w.setValue(self.w)
        self.pte_cn.setPlainText(self.cn)
