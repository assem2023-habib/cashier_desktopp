from PySide6.QtWidgets import QLineEdit
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt

from views.components.form_row import FormRow


class InputField(FormRow):
    def __init__(self, placeholder="", icon=None, parent=None):

        self.input = QLineEdit()
        self.input.setPlaceholderText(placeholder)
        self.input.setFixedHeight(44)

        self.input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #D1D5DB;
                border-radius: 8px;
                padding-left: 36px;
                padding-right: 12px;
                background: white;
                font-size: 14px;
                color: black;
            }
        """)

        if icon:
            act = QAction(icon, self.input)
            self.input.addAction(act, QLineEdit.LeadingPosition)

        # لا يوجد زر إضافي هنا، لذلك نمرر None
        super().__init__(self.input, None)

    # Helper methods (لتسهيل الربط مع ViewModel)
    def text(self):
        return self.input.text()

    def setText(self, t):
        self.input.setText(t)

    def textChanged(self, fn):
        self.input.textChanged.connect(fn)
