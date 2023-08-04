import json
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QLabel, QFormLayout, QSpinBox, QPushButton, QMessageBox
import publicData
init_w = 100  # 初始权重


class SeSe(QDialog):  # 设置
    def __init__(self):
        super(QDialog, self).__init__()
        self.setWindowIcon(publicData.icon)
        self.resize(200, 120)
        self.formLayout = QFormLayout(self)

        font = QFont()
        font.setPointSize(16)

        self.label = QLabel(self)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.sb_min = QSpinBox(self)
        self.sb_min.setAlignment(Qt.AlignCenter)
        self.sb_min.setMinimum(1)
        self.sb_min.setMaximum(360)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.sb_min)

        self.label_2 = QLabel(self)
        self.label_2.setFont(font)
        self.label_2.setAlignment(Qt.AlignCenter)
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.sb_num = QSpinBox(self)
        self.sb_num.setAlignment(Qt.AlignCenter)
        self.sb_num.setMinimum(1)
        self.sb_num.setMaximum(360)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.sb_num)

        self.label_3 = QLabel(self)
        self.label_3.setFont(font)
        self.label_3.setAlignment(Qt.AlignCenter)
        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.sb_size = QSpinBox(self)
        self.sb_size.setAlignment(Qt.AlignCenter)
        self.sb_size.setMinimum(1)
        self.sb_size.setMaximum(360)
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.sb_size)

        self.sb_min.setValue(publicData.settings['minute'])
        self.sb_num.setValue(publicData.settings['number'])
        self.sb_size.setValue(publicData.settings['pointsize'])

        self.setWindowTitle("设置")
        self.label.setText("间隔分钟数")
        self.label_2.setText("单次单词数")
        self.label_3.setText("字体大小")

        self.btn_reset_w = QPushButton("重置单词权重", self)
        self.btn_reset_w.setFont(font)
        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.btn_reset_w)
        self.btn_reset_w.clicked.connect(self.reset_w)

    def reset_w(self):
        ans = QMessageBox.question(self, "警告", "此操作不可逆！\n是否坚持执行重置单词权重？", QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)
        if ans == QMessageBox.Yes:
            for word in publicData.words:
                publicData.words[word][0] = init_w
            with open('easy_words.json', encoding='UTF-8') as f:
                add_words = json.load(f)
            for word in add_words:
                publicData.words[word] = [init_w, publicData.easy_words[word]]
            with open('words.json', 'w', encoding='utf-8') as f:
                json.dump(publicData.words, f, ensure_ascii=False)
            with open('easy_words.json', 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False)

    def closeEvent(self, event):
        publicData.settings['minute'] = self.sb_min.value()
        publicData.settings['number'] = self.sb_num.value()
        publicData.settings['pointsize'] = self.sb_size.value()
        with open('settings.json', 'w', encoding='utf-8') as f:
            json.dump(publicData.settings, f, ensure_ascii=False)
        publicData.tp.setToolTip(
            "单词弹弹弹\n间隔分钟数: " + str(publicData.settings['minute']) + "\n单次单词数: " + str(publicData.settings['number']))
        publicData.tp.a2.setEnabled(True)
