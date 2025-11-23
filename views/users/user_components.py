from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
    QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QFrame, 
    QAbstractItemView, QComboBox, QMessageBox
)
from PySide6.QtCore import Qt, Signal
from enums.user_role_enum import UserRole

# --- Constants for Styling (Reusing consistent styles) ---
COLOR_WHITE = "#FFFFFF"
COLOR_DARK_GREY = "#333333"
COLOR_LIGHT_GREY = "#9CA3AF"
COLOR_BORDER = "#D1D5DB"
COLOR_GREEN = "#28A745"
COLOR_RED = "#DC3545"
COLOR_NAVY = "#2F3C64"
FONT_FAMILY = "Sans-serif"

class UserTable(QWidget):
    editClicked = Signal(object) # User object
    deleteClicked = Signal(int) # user_id

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Header
        header_lbl = QLabel("Users")
        header_lbl.setStyleSheet(f"font-family: {FONT_FAMILY}; font-weight: bold; font-size: 16px; color: {COLOR_DARK_GREY};")
        layout.addWidget(header_lbl)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Username", "Role", "Actions"])
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        
        # Table Style
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {COLOR_WHITE};
                border: none;
                gridline-color: transparent;
                font-family: {FONT_FAMILY};
            }}
            QHeaderView::section {{
                background-color: {COLOR_WHITE};
                color: {COLOR_DARK_GREY};
                font-weight: bold;
                border: none;
                border-bottom: 2px solid #F0F0F0;
                padding: 12px;
                text-align: left;
            }}
            QTableWidget::item {{
                padding: 12px;
                color: {COLOR_DARK_GREY};
                border-bottom: 1px solid #F5F5F5;
            }}
            QTableWidget::item:selected {{
                background-color: #F0F9FF;
                color: {COLOR_DARK_GREY};
            }}
        """)
        layout.addWidget(self.table)
        
        # Keep track of user objects
        self.users = []

    def set_users(self, users):
        self.users = users
        self.table.setRowCount(len(users))
        for i, user in enumerate(users):
            # ID
            self.table.setItem(i, 0, QTableWidgetItem(str(user.id)))
            
            # Username
            self.table.setItem(i, 1, QTableWidgetItem(user.user_name))
            
            # Role
            role_str = user.role.value if hasattr(user.role, 'value') else str(user.role)
            self.table.setItem(i, 2, QTableWidgetItem(role_str))
            
            # Actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            actions_layout.setAlignment(Qt.AlignLeft)
            
            edit_btn = QPushButton("Edit")
            edit_btn.setCursor(Qt.PointingHandCursor)
            edit_btn.setStyleSheet(f"color: {COLOR_NAVY}; background: transparent; border: none; font-weight: bold; margin-right: 10px;")
            edit_btn.clicked.connect(lambda checked, u=user: self.editClicked.emit(u))
            
            delete_btn = QPushButton("Delete")
            delete_btn.setCursor(Qt.PointingHandCursor)
            delete_btn.setStyleSheet(f"color: {COLOR_RED}; background: transparent; border: none; font-weight: bold;")
            delete_btn.clicked.connect(lambda checked, uid=user.id: self.deleteClicked.emit(uid))
            
            actions_layout.addWidget(edit_btn)
            actions_layout.addWidget(delete_btn)
            self.table.setCellWidget(i, 3, actions_widget)

class AddEditUserDialog(QDialog):
    def __init__(self, parent=None, user=None):
        super().__init__(parent)
        self.user = user
        self.setWindowTitle("Edit User" if user else "Add New User")
        self.setFixedSize(400, 350)
        self.setStyleSheet(f"background-color: {COLOR_WHITE};")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Edit User" if user else "Add New User")
        title.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {COLOR_DARK_GREY}; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet(self._input_style())
        if user:
            self.username_input.setText(user.user_name)
        layout.addWidget(QLabel("Username"))
        layout.addWidget(self.username_input)
        
        # Role
        self.role_input = QComboBox()
        self.role_input.addItems([r.value for r in UserRole])
        self.role_input.setStyleSheet(self._input_style())
        if user:
            self.role_input.setCurrentText(user.role.value)
        layout.addWidget(QLabel("Role"))
        layout.addWidget(self.role_input)
        
        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password (leave empty to keep current)" if user else "Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(self._input_style())
        layout.addWidget(QLabel("Password"))
        layout.addWidget(self.password_input)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.setStyleSheet(f"background-color: {COLOR_LIGHT_GREY}; color: white; border-radius: 4px; padding: 8px 16px;")
        cancel_btn.clicked.connect(self.reject)
        
        save_btn = QPushButton("Save")
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.setStyleSheet(f"background-color: {COLOR_GREEN}; color: white; border-radius: 4px; padding: 8px 16px;")
        save_btn.clicked.connect(self.accept)
        
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)

    def _input_style(self):
        return f"""
            border: 1px solid {COLOR_BORDER};
            border-radius: 4px;
            padding: 8px;
            font-family: {FONT_FAMILY};
            color: {COLOR_DARK_GREY};
        """

    def get_data(self):
        return {
            "username": self.username_input.text(),
            "role": self.role_input.currentText(),
            "password": self.password_input.text()
        }
