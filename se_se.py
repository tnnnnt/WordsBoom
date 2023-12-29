import csv
import json
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QLabel, QFormLayout, QSpinBox, QMessageBox, QPushButton, QCheckBox
import public_data as pdt


class SeSe(QDialog):  # 设置
    def __init__(self):
        super(QDialog, self).__init__()
        self.setWindowIcon(pdt.icon)
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

        self.label_4 = QLabel(self)
        self.label_4.setFont(font)
        self.label_4.setAlignment(Qt.AlignCenter)
        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_4)

        self.sb_streak = QSpinBox(self)
        self.sb_streak.setAlignment(Qt.AlignCenter)
        self.sb_streak.setMinimum(1)
        self.sb_streak.setMaximum(20)
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.sb_streak)

        self.cb_confirm = QCheckBox(self)
        self.cb_confirm.setText("完全认识的确认")
        self.cb_confirm.setFont(font)
        self.cb_confirm.setTristate(False)  # 设置为不允许第三种状态
        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.cb_confirm)

        self.sb_min.setValue(pdt.settings['minute'])
        self.sb_num.setValue(pdt.settings['number'])
        self.sb_size.setValue(pdt.settings['pointsize'])
        self.sb_streak.setValue(pdt.settings['streak'])
        self.cb_confirm.setChecked(pdt.settings['confirm'])

        self.setWindowTitle("设置")
        self.label.setText("间隔分钟数")
        self.label_2.setText("单次单词数")
        self.label_3.setText("字体大小")
        self.label_4.setText("连续认识次数")

        self.btn_reset_w = QPushButton("重置单词权重", self)
        self.btn_reset_w.setFont(font)
        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.btn_reset_w)
        self.btn_reset_w.clicked.connect(self.reset_w)

        self.btn_sure = QPushButton("确认", self)
        self.btn_sure.setFont(font)
        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.btn_sure)
        self.btn_sure.clicked.connect(self.reset)

        self.btn_start = QPushButton("启动", self)
        self.btn_start.setFont(font)
        self.btn_start.setEnabled(False)
        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.btn_start)
        self.btn_start.clicked.connect(self.start_event)

        self.btn_cancel = QPushButton("取消", self)
        self.btn_cancel.setFont(font)
        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.btn_cancel)
        self.btn_cancel.clicked.connect(self.close)

    def reset_w(self):
        ans = QMessageBox.question(self, "警告", "此操作不可逆！\n是否坚持执行重置单词权重？",
                                   QMessageBox.Yes | QMessageBox.No,
                                   QMessageBox.No)
        if ans == QMessageBox.Yes:
            for word in pdt.words:
                pdt.words[word][0] = pdt.init_w
            with open('easy_words.json', encoding='utf-8') as f:
                add_words = json.load(f)
            for word in add_words:
                pdt.words[word] = [pdt.init_w, pdt.easy_words[word]]
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
            with open('easy_words.json', 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False)

    def reset(self):
        pdt.settings['minute'] = self.sb_min.value()
        pdt.settings['number'] = self.sb_num.value()
        pdt.settings['pointsize'] = self.sb_size.value()
        pdt.settings['streak'] = self.sb_streak.value()
        pdt.settings['confirm'] = self.cb_confirm.isChecked()
        with open('settings.json', 'w', encoding='utf-8') as f:
            json.dump(pdt.settings, f, ensure_ascii=False)
        pdt.tp.setToolTip("单词弹弹弹\n间隔分钟数: " + str(pdt.settings['minute']) + "\n单次单词数: " + str(
            pdt.settings['number']) + "\n剩余单词数: " + str(len(pdt.words)))
        self.btn_start.setEnabled(True)

    def closeEvent(self, event):
        pdt.tp.a1.setEnabled(True)
        pdt.tp.a2.setEnabled(True)

    def start_event(self):
        self.close()
        pdt.tp.a1.setText('暂停')
        pdt.tp.thread.start()
        pdt.tp.select()
