from PySide6.QtCore import QObject, Signal, Slot, Property
from sqlalchemy.orm import Session
from core.services.product_service import ProductService
from core.services.category_service import CategoryService
from core.repositories.category_repository import CategoryRepository
from models.product import Product
import math

class ProductViewModel(QObject):
    productsChanged = Signal()
    categoriesChanged = Signal()
    paginationChanged = Signal()
    isLoadingChanged = Signal(bool)
    errorChanged = Signal(str)
    successChanged = Signal(str)

    def __init__(self, db_session: Session):
        super().__init__()
        self.db_session = db_session
        self.product_service = ProductService(db_session)
        self.category_service = CategoryService(CategoryRepository(db_session))
        
        self._products = []
        self._categories = []
        self._current_page = 1
        self._per_page = 10
        self._total_items = 0
        self._total_pages = 0
        self._search_query = ""
        self._is_loading = False
        self._error = ""
        self._success = ""

        # Initial load
        self.load_products()
        self.load_categories()

    @Property(bool, notify=isLoadingChanged)
    def isLoading(self):
        return self._is_loading

    def set_is_loading(self, value):
        if self._is_loading != value:
            self._is_loading = value
            self.isLoadingChanged.emit(value)

    @Property(int, notify=paginationChanged)
    def currentPage(self):
        return self._current_page

    @Property(int, notify=paginationChanged)
    def totalPages(self):
        return self._total_pages

    @Property(int, notify=paginationChanged)
    def totalItems(self):
        return self._total_items
    
    @Property(str, notify=errorChanged)
    def error(self):
        return self._error
    
    @Property(str, notify=successChanged)
    def success(self):
        return self._success

    def get_products(self):
        return self._products
    
    def get_categories(self):
        return self._categories

    # We don't expose products as a simple property because it's a list of objects 
    # that might be complex to bind directly in some contexts, but for Python usage it's fine.
    # We'll use a getter for the view to access.

    @Slot()
    def load_products(self):
        self.set_is_loading(True)
        self._error = ""
        self.errorChanged.emit("")
        
        try:
            if self._search_query:
                # Search mode (client-side filtering for now as service search doesn't paginate)
                # Or we can update service to paginate search results. 
                # For now, let's use the service's search and manual pagination or just show all for search.
                # The prompt implies a robust system. Let's stick to simple pagination for main list
                # and maybe just list all for search for simplicity, or paginate search if possible.
                # Given time constraints, let's just use the search method and not paginate search results strictly,
                # or just slice them here.
                all_results = self.product_service.search_products(self._search_query)
                self._total_items = len(all_results)
                self._total_pages = math.ceil(self._total_items / self._per_page)
                
                start = (self._current_page - 1) * self._per_page
                end = start + self._per_page
                self._products = all_results[start:end]
            else:
                # Standard pagination
                self._products, self._total_items = self.product_service.get_products_paginated(
                    self._current_page, self._per_page
                )
                self._total_pages = math.ceil(self._total_items / self._per_page)

            self.productsChanged.emit()
            self.paginationChanged.emit()

        except Exception as e:
            self._error = str(e)
            self.errorChanged.emit(self._error)
        finally:
            self.set_is_loading(False)

    @Slot()
    def load_categories(self):
        try:
            self._categories = self.category_service.get_all_categories()
            self.categoriesChanged.emit()
        except Exception as e:
            print(f"Error loading categories: {e}")

    @Slot(str)
    def search(self, query):
        self._search_query = query
        self._current_page = 1 # Reset to first page on search
        self.load_products()

    @Slot()
    def nextPage(self):
        if self._current_page < self._total_pages:
            self._current_page += 1
            self.load_products()

    @Slot()
    def prevPage(self):
        if self._current_page > 1:
            self._current_page -= 1
            self.load_products()

    @Slot(str, str, str, str, int, str)
    def addProduct(self, name, barcode, price_str, quantity_str, category_id, low_stock_threshold):
        try:
            price = int(float(price_str)) # Handle potential float input
            quantity = int(quantity_str)
            
            # low_stock_threshold is ignored for persistence as per plan
            # but we accept it to match UI
            
            product = self.product_service.create_product(name, barcode, price, quantity, category_id)
            if product:
                self._success = "Product added successfully"
                self.successChanged.emit(self._success)
                self.load_products() # Refresh list
            else:
                self._error = "Failed to add product. Barcode might exist."
                self.errorChanged.emit(self._error)
        except ValueError as e:
            self._error = str(e)
            self.errorChanged.emit(self._error)
        except Exception as e:
            self._error = f"An error occurred: {str(e)}"
            self.errorChanged.emit(self._error)

    @Slot(int, str, str, str, str, int, str)
    def updateProduct(self, product_id, name, barcode, price_str, quantity_str, category_id, low_stock_threshold):
        try:
            price = int(float(price_str))
            quantity = int(quantity_str)
            
            product = self.product_service.update_product(product_id, name, barcode, price, quantity, category_id)
            if product:
                self._success = "Product updated successfully"
                self.successChanged.emit(self._success)
                self.load_products()
            else:
                self._error = "Failed to update product."
                self.errorChanged.emit(self._error)
        except ValueError as e:
            self._error = str(e)
            self.errorChanged.emit(self._error)
        except Exception as e:
            self._error = f"An error occurred: {str(e)}"
            self.errorChanged.emit(self._error)

    @Slot(int)
    def deleteProduct(self, product_id):
        if self.product_service.delete_product(product_id):
            self._success = "Product deleted successfully"
            self.successChanged.emit(self._success)
            # Adjust page if empty
            if len(self._products) == 1 and self._current_page > 1:
                self._current_page -= 1
            self.load_products()
        else:
            self._error = "Failed to delete product"
            self.errorChanged.emit(self._error)
