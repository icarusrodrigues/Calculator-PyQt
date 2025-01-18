from PySide6.QtWidgets import QLineEdit
from PySide6.QtCore import Qt, QLocale
from PySide6.QtGui import QDoubleValidator
from variables import BIG_FONT_SIZE, TEXT_MARGIN, MINIMUM_WIDTH

class Display(QLineEdit):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.configStyle()

        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        validator.setLocale(QLocale(QLocale.c()))
        self.setValidator(validator)

    def configStyle(self):
        self.setMinimumWidth(MINIMUM_WIDTH)
        self.setStyleSheet(f"font-size: {BIG_FONT_SIZE}px;")
        self.setMinimumHeight(BIG_FONT_SIZE * 2)
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.setTextMargins(*[TEXT_MARGIN] * 4)
