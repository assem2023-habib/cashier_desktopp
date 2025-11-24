from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.category import Category
from core.repositories.category_repository import CategoryRepository

class CategoryService:
    def __init__(self, db: Session):
        self.db = db
        self.category_repository = CategoryRepository(db)

    def create_category(self, name: str, description: str = None) -> Optional[Category]:
        try:
            if not name or not name.strip():
                raise ValueError("Category name is required")
            
            category = Category(name=name.strip(), description=description)
            category = self.category_repository.add(category)
            self.db.commit()
            return category
        except (SQLAlchemyError, ValueError) as e:
            self.db.rollback()
            raise

    def get_all_categories(self) -> List[Category]:
        try:
            return self.category_repository.list()
        except SQLAlchemyError:
            return []

    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        try:
            return self.category_repository.get(category_id)
        except SQLAlchemyError:
            return None

    def update_category(self, category_id: int, name: str, description: str = None) -> Optional[Category]:
        try:
            if not name or not name.strip():
                raise ValueError("Category name is required")
            
            category = self.category_repository.get(category_id)
            if not category:
                raise ValueError(f"Category {category_id} not found")
            
            category.name = name.strip()
            category.description = description
            category = self.category_repository.update(category)
            self.db.commit()
            return category
        except (SQLAlchemyError, ValueError) as e:
            self.db.rollback()
            raise

    def delete_category(self, category_id: int) -> bool:
        try:
            category = self.category_repository.get(category_id)
            if not category:
                return False
            
            success = self.category_repository.delete(category)
            if success:
                self.db.commit()
                return True
            return False
        except SQLAlchemyError:
            self.db.rollback()
            return False
