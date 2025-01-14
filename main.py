import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()

    label = QLabel("This is my text!")
    label.setStyleSheet("font-size: 50px;")

    window.v_layout.addWidget(label)

    window.adjustFixedSize()
    window.show()

    app.exec()
