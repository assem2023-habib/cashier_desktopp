from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QFont, QColor

class TitleLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        
        font = QFont("Sans", 24)
        font.setBold(True)
        self.setFont(font)
        self.setStyleSheet("color: #2F3C64;")


class SubtitleLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)

        font = QFont("Sans", 12)
        self.setFont(font)
        self.setStyleSheet("color: #6B7280;")