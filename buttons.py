from PySide6.QtWidgets import QPushButton, QGridLayout
from PySide6.QtCore import Slot
from variables import MEDIUM_FONT_SIZE
from utils import isNumOrDot, isValidNumber
from display import Display
from info import Info
from math import e, pow

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
        self._isEquationFinished = False

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

                self.addWidget(button, self._grid_mask.index(row), row.index(buttonText))

                if not isNumOrDot(buttonText):
                    button.setProperty("cssClass", "specialButton")
                    self._configSpecialButton(button)
                    continue

                slot = self._makeSlot(self._insertButtonTextToDisplay, button)
                self._connectButtonClicked(button, slot)
    
    def _connectButtonClicked(self, button, slot):
        button.clicked.connect(slot)

    def _configSpecialButton(self, button):
        text = button.text()

        if text == "C":
            self._connectButtonClicked(button, self._clear)

        if text == "◄":
            self._connectButtonClicked(button, self.display.backspace)

        if text in "+-*/^":
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

        if self._isEquationFinished and self._operator is None:
            self._clear()
        
        if buttonText == "." and len(self.display.text()) == 0:
            self.display.insert("0")
        
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
        self._isEquationFinished = False
        self.display.clear()

    def _operatorClicked(self, button):
        buttonText = button.text()
        displayText = self.display.text()

        if self._left is not None and self._operator is not None and isValidNumber(displayText):
            self._right = float(displayText)
            self._equal()

        self.display.clear()

        if not isValidNumber(displayText) and self._left is None:
            return

        if self._left is None:
            self._left = float(displayText)
        
        self._operator = buttonText
        self.equation = f"{self._left} {self._operator} ??"

    def _equal(self):
        if self._left is None or self._operator is None:
            return
        
        displayText = self.display.text()

        if not isValidNumber(displayText):
            return
        
        self._right = float(displayText)
        self.equation = f"{self._left} {self._operator} {self._right}"
        result = 0.0

        try:
            if "^" in self._operator:
                result = pow(self._left, self._right)
            else:
                result = eval(self.equation)
        except ZeroDivisionError:
            self.display.setText("Division by zero")
            return
        except OverflowError:
            self.display.setText("Too large number")
            return

        self.display.setText(str(result))
        self.equation = f"{self._left} {self._operator} {self._right} = {result}"
        self._left = result
        self._right = None
        self._operator = None
        self._isEquationFinished = True
        self.display.clear()
