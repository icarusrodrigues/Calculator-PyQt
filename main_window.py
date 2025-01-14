from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout

class MainWindow(QMainWindow):
    def __init__ (self, parent: QWidget| None = None, *args, **kwargs) -> None:
        super().__init__(parent, *args, **kwargs)

        self.cw = QWidget()
        self.vLayout = QVBoxLayout()
        
        self.cw.setLayout(self.vLayout)

        self.setCentralWidget(self.cw)
        self.setWindowTitle("Calculator")

    def adjustFixedSize(self):
        self.adjustSize()
        self.setFixedSize(self.width(), self.height())

    def addWidgetToVLayout(self, widget):
        self.vLayout.addWidget(widget)
