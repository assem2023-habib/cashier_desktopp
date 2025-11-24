from typing import List
from models.category import Category
from core.abstracts.category_repository import ICategoryRepository

class CategoryService:
    def __init__(self, category_repository: ICategoryRepository):
        self.category_repository = category_repository

    def create_category(self, name: str, description: str = None) -> Category:
        category = Category(name=name, description=description)
        return self.category_repository.add(category)

    def get_all_categories(self) -> List[Category]:
        return self.category_repository.list()

    def get_category_by_id(self, category_id: int) -> Category:
        return self.category_repository.get(category_id)

    def update_category(self, category_id: int, name: str, description: str = None) -> Category:
        category = self.category_repository.get(category_id)
        if category:
            category.name = name
            category.description = description
            return self.category_repository.update(category)
        return None

    def delete_category(self, category_id: int) -> bool:
        category = self.category_repository.get(category_id)
        if category:
            return self.category_repository.delete(category)
        return False
