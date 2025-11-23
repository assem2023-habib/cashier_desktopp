from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QLabel
)
from PySide6.QtCore import Qt

from viewmodels.users.user_viewmodel import UserViewModel
from views.users.user_components import UserTable, AddEditUserDialog
from views.products.product_components import PaginationControls # Reuse pagination
from data.database import SessionLocal

class UserManagementView(QWidget):
    def __init__(self):
        super().__init__()
        
        # Initialize ViewModel
        self.db_session = SessionLocal()
        self.vm = UserViewModel(self.db_session)
        
        self._build_ui()
        self._bind_viewmodel()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Top Bar (Title + Add Button)
        top_layout = QHBoxLayout()
        title = QLabel("User Management")
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        top_layout.addWidget(title)
        
        top_layout.addStretch()
        
        self.add_btn = QPushButton("+ Add New User")
        self.add_btn.setCursor(Qt.PointingHandCursor)
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #2F3C64;
                color: white;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1a2540;
            }
        """)
        top_layout.addWidget(self.add_btn)
        layout.addLayout(top_layout)
        
        # User Table
        self.table = UserTable()
        layout.addWidget(self.table)
        
        # Pagination
        self.pagination = PaginationControls()
        layout.addWidget(self.pagination)

    def _bind_viewmodel(self):
        # View -> ViewModel
        self.add_btn.clicked.connect(self._show_add_dialog)
        self.table.editClicked.connect(self._show_edit_dialog)
        self.table.deleteClicked.connect(self._confirm_delete)
        
        self.pagination.prevClicked.connect(self.vm.prevPage)
        self.pagination.nextClicked.connect(self.vm.nextPage)
        
        # ViewModel -> View
        self.vm.usersChanged.connect(self._update_table)
        self.vm.paginationChanged.connect(self._update_pagination)
        self.vm.errorChanged.connect(self._show_error)
        self.vm.successChanged.connect(self._show_success)
        
        # Initial State
        self._update_table()
        self._update_pagination()

    def _update_table(self):
        self.table.set_users(self.vm.get_users())

    def _update_pagination(self):
        self.pagination.update_state(
            self.vm.currentPage,
            self.vm.totalPages,
            self.vm.totalItems,
            self.vm._per_page
        )

    def _show_add_dialog(self):
        dialog = AddEditUserDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            self.vm.addUser(data['username'], data['password'], data['role'])

    def _show_edit_dialog(self, user):
        dialog = AddEditUserDialog(self, user)
        if dialog.exec():
            data = dialog.get_data()
            self.vm.updateUser(user.id, data['username'], data['role'], data['password'])

    def _confirm_delete(self, user_id):
        reply = QMessageBox.question(
            self, "Confirm Delete", 
            "Are you sure you want to delete this user?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.vm.deleteUser(user_id)

    def _show_error(self, message):
        if message:
            QMessageBox.warning(self, "Error", message)

    def _show_success(self, message):
        if message:
            QMessageBox.information(self, "Success", message)
