from PySide6.QtWidgets import QFrame, QGraphicsDropShadowEffect, QVBoxLayout
from PySide6.QtGui import QColor

class CardWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 18px;
            }
        """)
        
        # Shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(8)
        shadow.setColor(QColor(0, 0, 0, 25)) # rgba(0, 0, 0, 0.1) is approx 25 alpha
        self.setGraphicsEffect(shadow)
        
        # Layout for the card content
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(40, 40, 40, 40) # Consistent padding
        self.layout.setSpacing(20)

    def addWidget(self, widget):
        self.layout.addWidget(widget)

    def addLayout(self, layout):
        self.layout.addLayout(layout)
