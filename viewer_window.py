import csv
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QDialog, QVBoxLayout, QScrollArea, QWidget, QHBoxLayout, QSizePolicy, QPushButton
import public_data as pdt
from PyQt5.QtCore import Qt
from edit_word import EditWord


def add_word():
    pdt.word_editing.set_self('新建单词', '', 100, '')
    pdt.word_editing.show()


class ViewerWindow(QDialog):
    def __init__(self):
        super(QDialog, self).__init__()
        self.resize(1314, 520)
        self.setWindowFlags(Qt.FramelessWindowHint)  # 去掉关闭按钮
        self.h = QVBoxLayout(self)

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
        self.h.addWidget(self.scrollArea)

        font = QFont()
        font.setPointSize(16)
        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)

        self.h_flag = QHBoxLayout()
        self.w_flag = QWidget()
        self.w_flag.setLayout(self.h_flag)
        self.h1 = QHBoxLayout()
        self.h2 = QHBoxLayout()
        self.w1 = QWidget()
        self.w1.setLayout(self.h1)
        self.w2 = QWidget()
        self.w2.setLayout(self.h2)
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
        self.label_empty = QLabel(self)
        size_policy.setHeightForWidth(self.label_empty.sizePolicy().hasHeightForWidth())
        self.label_empty.setSizePolicy(size_policy)
        self.label_empty.setFont(font)
        self.label_empty.setTextFormat(Qt.AutoText)
        self.label_empty.setAlignment(Qt.AlignCenter)

        self.label_eng.setText('英文')
        self.label_w.setText('权重')
        self.label_cn.setText('中文')

        self.h2.addWidget(self.label_empty)
        self.h2.addWidget(self.label_empty)
        self.h_flag.addWidget(self.w1)
        self.h_flag.addWidget(self.label_cn)
        self.h_flag.addWidget(self.w2)
        self.verticalLayout_2.addWidget(self.w_flag)

        self.edit_words = {}
        for word in pdt.words:
            self.edit_words[word] = EditWord(word)
            self.verticalLayout_2.addWidget(self.edit_words[word])

        self.w_btn = QWidget()
        self.h_btn = QHBoxLayout()
        self.w_btn.setLayout(self.h_btn)
        self.btn_add = QPushButton('添加')
        self.btn_save = QPushButton('保存并退出')
        self.h_btn.addWidget(self.btn_add)
        self.h_btn.addWidget(self.btn_save)
        self.h.addWidget(self.w_btn)

        self.btn_add.clicked.connect(add_word)
        self.btn_save.clicked.connect(self.close)

    def closeEvent(self, event):
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
        pdt.tp.a3.setEnabled(True)
