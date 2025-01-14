import sys
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from main_window import MainWindow
from variables import WINDOW_ICON
from display import Display

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()

    icon = QIcon(str(WINDOW_ICON))
    window.setWindowIcon(icon)
    app.setWindowIcon(icon)

    display = Display("Initial text")
    window.addWidgetToVLayout(display)

    window.adjustFixedSize()
    window.show()
    app.exec()
