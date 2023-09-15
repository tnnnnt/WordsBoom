import json
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSizePolicy, QLabel, QPushButton, QMessageBox
import public_data as pdt

disunderstand, fuzzy, know = 10, 2, -5  # 权重变化


class OneWord(QWidget):
    def __init__(self, word):
        super(QWidget, self).__init__()
        self.word = word
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        font = QFont()
        font.setPointSize(pdt.settings['pointsize'])
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

        # 给定数值，用于控制背景色
        value = 0.1  # 假设这是一个范围在0到1之间的值

        # 计算背景色，根据数值越大越红
        red_value = int(value * 255)  # 将0-1的值映射到0-255的红色范围
        background_color = QColor(red_value, 0, 0)  # 创建颜色对象

        # 生成样式表，设置背景色
        style_sheet = f'background-color: {background_color.name()};'
        self.label.setStyleSheet(style_sheet)

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
        self.pushButton.setText(pdt.words[self.word][1])
        self.pushButton.setEnabled(False)

    # 不认识
    def btn_disunderstand(self):
        pdt.words[self.word][0] += disunderstand
        pdt.hard_words[self.word] = pdt.settings['streak']
        # 更新困难词
        with open('hard_words.json', 'w', encoding='utf-8') as f:
            json.dump(pdt.hard_words, f, ensure_ascii=False)
        self.close()
        del self

    # 模糊
    def btn_fuzzy(self):
        pdt.words[self.word][0] += fuzzy
        pdt.hard_words[self.word] = pdt.settings['streak']
        # 更新困难词
        with open('hard_words.json', 'w', encoding='utf-8') as f:
            json.dump(pdt.hard_words, f, ensure_ascii=False)
        self.close()
        del self

    # 认识
    def btn_know(self):
        pdt.words[self.word][0] += know
        if pdt.words[self.word][0] <= 0:
            pdt.words[self.word][0] = 1
        if self.word in pdt.hard_words:
            pdt.hard_words[self.word] -= 1
            if pdt.hard_words[self.word] == 0:
                pdt.hard_words.pop(self.word)
            # 更新困难词
            with open('hard_words.json', 'w', encoding='utf-8') as f:
                json.dump(pdt.hard_words, f, ensure_ascii=False)
        self.close()
        del self

    # 完全认识
    def del_word(self):
        if pdt.settings['confirm']:
            ans = QMessageBox.question(self, "提示", "你真的完全认识了吗？", QMessageBox.Yes | QMessageBox.No,
                                       QMessageBox.No)
            if ans == QMessageBox.No:
                return
        pdt.easy_words[self.word] = pdt.words[self.word][1]
        with open('easy_words.json', 'w', encoding='utf-8') as f:
            json.dump(pdt.easy_words, f, ensure_ascii=False)
        if self.word in pdt.hard_words:
            pdt.hard_words.pop(self.word)
            # 更新困难词
            with open('hard_words.json', 'w', encoding='utf-8') as f:
                json.dump(pdt.hard_words, f, ensure_ascii=False)
        pdt.tp.sw.del_words.append(self.word)
        self.close()
        del self

    def closeEvent(self, event):
        pdt.tp.sw.ow_count -= 1
        if pdt.tp.sw.ow_count == 0:
            pdt.tp.sw.close()
