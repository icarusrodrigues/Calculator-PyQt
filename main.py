import sys
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from buttons import ButtonsGrid
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

    info = Info("")
    window.addWidgetToVLayout(info)
    
    display = Display()
    window.addWidgetToVLayout(display)

    buttonsGrid = ButtonsGrid(display, info, window)
    window.vLayout.addLayout(buttonsGrid)

    window.adjustFixedSize()
    window.show()
    app.exec()
