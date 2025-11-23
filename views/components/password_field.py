from PySide6.QtWidgets import QLineEdit, QToolButton
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt

from views.components.form_row import FormRow


class PasswordField(FormRow):
    def __init__(self, placeholder="", icon="🔒", parent=None):
        
        self.input = QLineEdit()
        self.input.setPlaceholderText(placeholder)
        self.input.setEchoMode(QLineEdit.Password)
        self.input.setFixedHeight(44)
        
        self.input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                padding-left: 36px;
                padding-right: 12px;
                background: white;
                color: black;
                font-size: 14px;
            }
        """)

        act = QAction(icon, self.input)
        self.input.addAction(act, QLineEdit.LeadingPosition)

        # Eye button
        self.eye_btn = QToolButton()
        self.eye_btn.setText("👁")
        self.eye_btn.setCheckable(True)
        self.eye_btn.setCursor(Qt.PointingHandCursor)

        super().__init__(self.input, self.eye_btn)

        self.eye_btn.toggled.connect(self._toggle)

    def _toggle(self, state):
        self.input.setEchoMode(QLineEdit.Normal if state else QLineEdit.Password)

    # Helpers to allow ViewModel binding
    def text(self):
        return self.input.text()

    def setText(self, t):
        self.input.setText(t)

    def textChanged(self, fn):
        self.input.textChanged.connect(fn)
