from PySide6.QtWidgets import QPushButton, QGridLayout
from PySide6.QtCore import Slot
from variables import MEDIUM_FONT_SIZE
from utils import isNumOrDot, isEmpty, isValidNumber
from display import Display
from info import Info
from math import e

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from display import Display
    from info import Info

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
    def __init__(self, display: "Display", info: "Info", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._grid_mask = [
            ["C", "◄", "^", "/"],
            ["7", "8", "9", "*"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "+"],
            ["e", "0", ".", "="]
        ]
        self.display = display
        self.info = info
        self._equation = ""
        self._left = None
        self._right = None
        self._operator = None

        self._makeGrid()
    
    @property
    def equation(self):
        return self._equation
    
    @equation.setter
    def equation(self, value):
        self._equation = value
        self.info.setText(value)

    def _makeGrid(self):
        for row in self._grid_mask:
            for buttonText in row:
                button = Button(buttonText)

                if not isNumOrDot(buttonText) and not isEmpty(buttonText):
                    button.setProperty("cssClass", "specialButton")
                    self._configSpecialButton(button)

                self.addWidget(button, self._grid_mask.index(row), row.index(buttonText))

                slot = self._makeSlot(self._insertButtonTextToDisplay, button)
                self._connectButtonClicked(button, slot)
    
    def _connectButtonClicked(self, button, slot):
        button.clicked.connect(slot)

    def _configSpecialButton(self, button):
        text = button.text()

        if text == "C":
            self._connectButtonClicked(button, self._clear)

        if text in "+-*/":
            self._connectButtonClicked(button, self._makeSlot(self._operatorClicked, button))

        if text == "=":
            self._connectButtonClicked(button, self._equal)

    def _makeSlot(self, method, *args, **kwargs):
        @Slot()
        def realSlot():
            method(*args, **kwargs)
        return realSlot
        
    def _insertButtonTextToDisplay(self, button):
        buttonText = button.text()
        newDisplayValue = self.display.text() + buttonText

        if not isValidNumber(newDisplayValue):
            return

        if buttonText == "e":
            self.display.insert(str(e))
            return

        self.display.insert(buttonText)

    def _clear(self):
        self._left = None
        self._right = None
        self._operator = None
        self.equation = ""
        self.display.clear()

    def _operatorClicked(self, button):
        buttonText = button.text()
        displayText = self.display.text()
        self.display.clear()

        if not isValidNumber(displayText) and self._left is None:
            return

        if self._left is None:
            self._left = displayText
        
        self._operator = buttonText
        self.equation = f"{self._left} {self._operator} ??"

    def _equal(self):
        displayText = self.display.text()

        if not isValidNumber(displayText):
            return
        
        self._right = float(displayText)
        self.equation = f"{self._left} {self._operator} {self._right}"
        result = 0.0

        try:
            result = eval(self.equation)
        except ZeroDivisionError:
            self.display.setText("Division by zero")
            return
        
        self.display.setText(str(result))
        self.equation = f"{self._left} {self._operator} {self._right} = {result}"
        self._left = result
