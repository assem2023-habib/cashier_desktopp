from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox
from PySide6.QtCore import Qt
from viewmodels.categories.category_viewmodel import CategoryViewModel
from views.categories.category_components import CategoryTable, AddEditCategoryDialog

class CategoryManagementView(QWidget):
    def __init__(self, viewmodel: CategoryViewModel):
        super().__init__()
        self.viewmodel = viewmodel
        
        # Layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(30, 30, 30, 30)
        self.layout.setSpacing(20)
        
        # Top Bar (Add Button)
        top_bar = QHBoxLayout()
        top_bar.addStretch()
        
        self.add_btn = QPushButton("Add New Category")
        self.add_btn.setCursor(Qt.PointingHandCursor)
        self.add_btn.setStyleSheet("""
            QPushButton {
                background-color: #28A745;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-family: Sans-serif;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        self.add_btn.clicked.connect(self._show_add_dialog)
        top_bar.addWidget(self.add_btn)
        
        self.layout.addLayout(top_bar)
        
        # Table
        self.table = CategoryTable()
        self.table.editClicked.connect(self._show_edit_dialog)
        self.table.deleteClicked.connect(self._delete_category)
        self.layout.addWidget(self.table)
        
        # Connect ViewModel signals
        self.viewmodel.categoriesChanged.connect(self._update_table)
        self.viewmodel.errorOccurred.connect(self._show_error)
        
        # Initial Load
        self.viewmodel.load_categories()

    def _update_table(self):
        self.table.set_categories(self.viewmodel.categories)

    def _show_add_dialog(self):
        dialog = AddEditCategoryDialog(self)
        if dialog.exec():
            data = dialog.get_data()
            self.viewmodel.add_category(data["name"])

    def _show_edit_dialog(self, category):
        dialog = AddEditCategoryDialog(self, category)
        if dialog.exec():
            data = dialog.get_data()
            self.viewmodel.update_category(category.id, data["name"])

    def _delete_category(self, category_id):
        reply = QMessageBox.question(
            self, "Confirm Delete", 
            "Are you sure you want to delete this category?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.viewmodel.delete_category(category_id)

    def _show_error(self, message):
        QMessageBox.critical(self, "Error", message)
