import argparse
import sys
import threading
import time

from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QPushButton, QLabel, QVBoxLayout, QWidget, QApplication, QMessageBox
from PyQt5.QtGui import QFont
from backend import backend

class MainWindow(QWidget):
    def __init__(self, target_lang):
        super().__init__()
        self.row = 0
        self.labels = []
        self.setWindowTitle("My App")
        self.setAttribute(Qt.WA_TranslucentBackground, on = True)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setGeometry(50, 50, 100, 100)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.show()

        self.worker = backend(target_lang)
        self.worker.start()
        self.worker.finished.connect(self.finish_message)
        self.worker.update_progress.connect(self.append)

    def finish_message(self):
        QMessageBox.information(self, "Done", "Worker thread complete")

    def append(self, message=0):
        self.label = QLabel(str(message))

        self.label.setFont(QFont('Times', 11))
        self.label.setStyleSheet("color:white;")
        self.labels.append(self.label)
        self.layout.addWidget(self.label)
        self.update()
        threading.Thread(target = self.remove, args=[self.labels[-1]]).start()

    def remove(self, label):
        time.sleep(5)
        self.layout.removeWidget(label)
        self.labels.remove(label)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--lang", type=str, required=True)
    args = parser.parse_args()
    app = QApplication(sys.argv)
    window = MainWindow(args.lang)
    app.exec_()