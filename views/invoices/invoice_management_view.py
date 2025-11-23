from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from PySide6.QtCore import Qt

from viewmodels.invoices.invoice_viewmodel import InvoiceViewModel
from views.invoices.invoice_components import (
    InvoiceSearchBar, InvoiceTable, InvoiceDetailDialog
)
from views.products.product_components import PaginationControls # Reuse pagination
from data.database import SessionLocal

class InvoiceManagementView(QWidget):
    def __init__(self):
        super().__init__()
        
        # Initialize ViewModel
        self.db_session = SessionLocal()
        self.vm = InvoiceViewModel(self.db_session)
        
        self._build_ui()
        self._bind_viewmodel()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Search Bar
        self.search_bar = InvoiceSearchBar()
        layout.addWidget(self.search_bar)
        
        # Invoice Table
        self.table = InvoiceTable()
        layout.addWidget(self.table)
        
        # Pagination
        self.pagination = PaginationControls()
        layout.addWidget(self.pagination)

    def _bind_viewmodel(self):
        # View -> ViewModel
        self.search_bar.searchChanged.connect(self.vm.search)
        
        self.table.viewDetailsClicked.connect(self.vm.loadInvoiceDetails)
        
        self.pagination.prevClicked.connect(self.vm.prevPage)
        self.pagination.nextClicked.connect(self.vm.nextPage)
        
        # ViewModel -> View
        self.vm.invoicesChanged.connect(self._update_table)
        self.vm.paginationChanged.connect(self._update_pagination)
        self.vm.errorChanged.connect(self._show_error)
        self.vm.successChanged.connect(self._show_success)
        self.vm.invoiceDetailsLoaded.connect(self._show_details_dialog)
        
        # Initial State
        self._update_table()
        self._update_pagination()

    def _update_table(self):
        self.table.set_invoices(self.vm.get_invoices())

    def _update_pagination(self):
        self.pagination.update_state(
            self.vm.currentPage,
            self.vm.totalPages,
            self.vm.totalItems,
            self.vm._per_page
        )

    def _show_details_dialog(self, details):
        dialog = InvoiceDetailDialog(self, details)
        dialog.exec()

    def _show_error(self, message):
        if message:
            QMessageBox.warning(self, "Error", message)

    def _show_success(self, message):
        if message:
            QMessageBox.information(self, "Success", message)
