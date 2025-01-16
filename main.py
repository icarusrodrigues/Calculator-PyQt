import sys
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from buttons import Button
from main_window import MainWindow
from variables import WINDOW_ICON
from display import Display
from info import Info
from styles import setupTheme

if __name__ == "__main__":
    app = QApplication(sys.argv)
    setupTheme(app)
    window = MainWindow()

    icon = QIcon(str(WINDOW_ICON))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    info = Info("2.0 ^ 10.0 = 1024.0")
    window.addWidgetToVLayout(info)
    
    display = Display()
    window.addWidgetToVLayout(display)

    button = Button("Texto do botão")
    window.addWidgetToVLayout(button)

    window.adjustFixedSize()
    window.show()
    app.exec()
