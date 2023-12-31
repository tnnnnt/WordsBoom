from PyQt5.QtCore import QObject, pyqtSignal


class Work(QObject):
    signal = pyqtSignal()

    def __init__(self):
        super(QObject, self).__init__()

    def do_work(self):
        self.signal.emit()
