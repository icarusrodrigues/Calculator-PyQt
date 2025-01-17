from PySide6.QtWidgets import QPushButton, QGridLayout
from PySide6.QtCore import Slot
from variables import MEDIUM_FONT_SIZE
from utils import isNumOrDot, isEmpty
from display import Display

class Button(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configStyle()

    def configStyle(self):
        font = self.font()
        font.setPixelSize(MEDIUM_FONT_SIZE)
        self.setFont(font)
        self.setMinimumSize(75, 75)

class ButtonsGrid(QGridLayout):
    def __init__(self, display: Display, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._grid_mask = [
            ["C", "◄", "^", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["e", "0", ".", "="]
        ]
        self.display = display
        self._makeGrid()

    def _makeGrid(self):
        for row in self._grid_mask:
            for buttonText in row:
                button = Button(buttonText)

                if not isNumOrDot(buttonText) and not isEmpty(buttonText):
                    button.setProperty("cssClass", "specialButton")

                self.addWidget(button, self._grid_mask.index(row), row.index(buttonText))

                buttonSlot = self._makeButtonDisplayConnection(
                    self._insertButtonTextToDisplay, button,
                )
                button.clicked.connect(buttonSlot)
    
    def _makeButtonDisplayConnection(self, method, *args, **kwargs):
        @Slot()
        def realSlot():
            method(*args, **kwargs)
        return realSlot
        

    def _insertButtonTextToDisplay(self, button):
        self.display.insert(button.text())
