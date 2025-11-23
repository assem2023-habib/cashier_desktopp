from PySide6.QtWidgets import QWidget, QHBoxLayout

class FormRow(QWidget):
    def __init__(self, left_widget, right_widget=None, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        layout.addWidget(left_widget)

        if right_widget:
            layout.addWidget(right_widget)