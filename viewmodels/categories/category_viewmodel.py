from PySide6.QtCore import QObject, Signal
from core.services.category_service import CategoryService

class CategoryViewModel(QObject):
    categoriesChanged = Signal()
    errorOccurred = Signal(str)

    def __init__(self, category_service: CategoryService):
        super().__init__()
        self.category_service = category_service
        self.categories = []

    def load_categories(self):
        try:
            self.categories = self.category_service.get_all_categories()
            self.categoriesChanged.emit()
        except Exception as e:
            self.errorOccurred.emit(str(e))

    def add_category(self, name, description=None):
        try:
            if not name:
                raise ValueError("Category name is required")
            
            self.category_service.create_category(name, description)
            self.load_categories()
        except Exception as e:
            self.errorOccurred.emit(str(e))

    def update_category(self, category_id, name, description=None):
        try:
            if not name:
                raise ValueError("Category name is required")
            
            self.category_service.update_category(category_id, name, description)
            self.load_categories()
        except Exception as e:
            self.errorOccurred.emit(str(e))

    def delete_category(self, category_id):
        try:
            self.category_service.delete_category(category_id)
            self.load_categories()
        except Exception as e:
            self.errorOccurred.emit(str(e))
