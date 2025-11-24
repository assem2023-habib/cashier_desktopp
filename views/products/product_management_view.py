from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from PySide6.QtCore import Qt

from viewmodels.products.product_viewmodel import ProductViewModel
from views.products.product_components import (
    ProductSearchBar, ProductTable, PaginationControls, AddEditProductDialog
)
from data.database import SessionLocal

class ProductManagementView(QWidget):
    def __init__(self):
        super().__init__()
        
        # Initialize ViewModel
        self.db_session = SessionLocal()
        self.vm = ProductViewModel(self.db_session)
        
        self._build_ui()
        self._bind_viewmodel()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Search Bar
        self.search_bar = ProductSearchBar()
        layout.addWidget(self.search_bar)
        
        # Product Table
        self.table = ProductTable()
        layout.addWidget(self.table)
        
        # Pagination
        self.pagination = PaginationControls()
        layout.addWidget(self.pagination)

    def _bind_viewmodel(self):
        # View -> ViewModel
        self.search_bar.searchChanged.connect(self.vm.search)
        self.search_bar.addProductClicked.connect(self._open_add_dialog)
        
        self.table.editProductClicked.connect(self._open_edit_dialog)
        self.table.deleteProductClicked.connect(self._confirm_delete)
        
        self.pagination.prevClicked.connect(self.vm.prevPage)
        self.pagination.nextClicked.connect(self.vm.nextPage)
        
        # ViewModel -> View
        self.vm.productsChanged.connect(self._update_table)
        self.vm.paginationChanged.connect(self._update_pagination)
        self.vm.errorChanged.connect(self._show_error)
        self.vm.successChanged.connect(self._show_success)
        
        # Initial State
        self._update_table()
        self._update_pagination()

    def _update_table(self):
        self.table.set_products(self.vm.get_products())

    def _update_pagination(self):
        self.pagination.update_state(
            self.vm.currentPage,
            self.vm.totalPages,
            self.vm.totalItems,
            self.vm._per_page # Accessing internal for simplicity, or expose property
        )

    def _open_add_dialog(self):
        dialog = AddEditProductDialog(self, categories=self.vm.get_categories())
        if dialog.exec():
            data = dialog.get_data()
            self.vm.addProduct(
                data["name"],
                data["price"],
                data["quantity"],
                data["category_id"],
                data["low_stock_threshold"]
            )

    def _open_edit_dialog(self, product_id):
        # Find product object
        product = next((p for p in self.vm.get_products() if p.id == product_id), None)
        if not product:
            return
            
        dialog = AddEditProductDialog(self, product, categories=self.vm.get_categories())
        if dialog.exec():
            data = dialog.get_data()
            self.vm.updateProduct(
                product_id,
                data["name"],
                product.barcode,  # Keep original barcode (immutable)
                data["price"],
                data["quantity"],
                data["category_id"],
                data["low_stock_threshold"]
            )

    def _confirm_delete(self, product_id):
        msg = QMessageBox(self)
        msg.setWindowTitle("Confirm Delete")
        msg.setText("Are you sure you want to delete this product?")
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)
        self._apply_msg_box_style(msg)
        
        if msg.exec() == QMessageBox.Yes:
            self.vm.deleteProduct(product_id)

    def _show_error(self, message):
        if message:
            msg = QMessageBox(self)
            msg.setWindowTitle("Error")
            msg.setText(message)
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            self._apply_msg_box_style(msg)
            msg.exec()

    def _show_success(self, message):
        if message:
            msg = QMessageBox(self)
            msg.setWindowTitle("Success")
            msg.setText(message)
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Ok)
            self._apply_msg_box_style(msg)
            msg.exec()

    def _apply_msg_box_style(self, msg_box):
        msg_box.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QMessageBox QLabel {
                color: #333333;
                font-family: Sans-serif;
                font-size: 14px;
            }
            QPushButton {
                background-color: #2F3C64;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 12px;
                font-family: Sans-serif;
                font-size: 12px;
                min-width: 60px;
            }
            QPushButton:hover {
                background-color: #1E2A47;
            }
        """)
