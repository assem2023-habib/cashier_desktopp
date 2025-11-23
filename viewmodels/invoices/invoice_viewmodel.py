from PySide6.QtCore import QObject, Signal, Slot, Property
from typing import List, Optional, Dict
from core.services.invoice_service import InvoiceService
from models.invoice import Invoice
from sqlalchemy.orm import Session
import math

class InvoiceViewModel(QObject):
    invoicesChanged = Signal()
    paginationChanged = Signal()
    isLoadingChanged = Signal(bool)
    errorChanged = Signal(str)
    successChanged = Signal(str)
    
    # Signal to notify when details are loaded
    invoiceDetailsLoaded = Signal(dict) 

    def __init__(self, db_session: Session):
        super().__init__()
        self.db_session = db_session
        self.invoice_service = InvoiceService(db_session)
        
        self._invoices = []
        self._current_page = 1
        self._per_page = 10
        self._total_items = 0
        self._total_pages = 0
        self._search_query = ""
        self._is_loading = False
        self._error = ""
        self._success = ""

        # Initial load
        self.load_invoices()

    @Property(bool, notify=isLoadingChanged)
    def isLoading(self):
        return self._is_loading

    @isLoading.setter
    def isLoading(self, value):
        if self._is_loading != value:
            self._is_loading = value
            self.isLoadingChanged.emit(value)

    @Property(str, notify=errorChanged)
    def error(self):
        return self._error
    
    @error.setter
    def error(self, value):
        if self._error != value:
            self._error = value
            self.errorChanged.emit(value)

    @Property(str, notify=successChanged)
    def success(self):
        return self._success
    
    @success.setter
    def success(self, value):
        if self._success != value:
            self._success = value
            self.successChanged.emit(value)

    @Property(int, notify=paginationChanged)
    def currentPage(self):
        return self._current_page

    @Property(int, notify=paginationChanged)
    def totalPages(self):
        return self._total_pages
    
    @Property(int, notify=paginationChanged)
    def totalItems(self):
        return self._total_items

    def get_invoices(self) -> List[Invoice]:
        return self._invoices

    @Slot()
    def load_invoices(self):
        self.isLoading = True
        self.error = ""
        try:
            if self._search_query:
                # Search mode (no pagination for now in search as per service implementation)
                self._invoices = self.invoice_service.search_invoices(self._search_query)
                self._total_items = len(self._invoices)
                self._total_pages = 1
            else:
                # Pagination mode
                self._invoices, self._total_items = self.invoice_service.get_invoices_paginated(
                    self._current_page, self._per_page
                )
                self._total_pages = math.ceil(self._total_items / self._per_page) if self._total_items > 0 else 1
            
            self.invoicesChanged.emit()
            self.paginationChanged.emit()
            
        except Exception as e:
            self.error = f"Failed to load invoices: {str(e)}"
        finally:
            self.isLoading = False

    @Slot(str)
    def search(self, query: str):
        self._search_query = query.strip()
        self._current_page = 1 # Reset to first page on search
        self.load_invoices()

    @Slot()
    def nextPage(self):
        if self._current_page < self._total_pages:
            self._current_page += 1
            self.load_invoices()

    @Slot()
    def prevPage(self):
        if self._current_page > 1:
            self._current_page -= 1
            self.load_invoices()

    @Slot(int)
    def loadInvoiceDetails(self, invoice_id: int):
        self.isLoading = True
        try:
            details = self.invoice_service.get_invoice_with_details(invoice_id)
            if details:
                self.invoiceDetailsLoaded.emit(details)
            else:
                self.error = "Invoice details not found"
        except Exception as e:
            self.error = f"Failed to load details: {str(e)}"
        finally:
            self.isLoading = False
