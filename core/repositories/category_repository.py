from sqlalchemy.orm import Session
from models.category import Category
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from core.abstracts.category_repository import ICategoryRepository

class CategoryRepository(ICategoryRepository):
    def __init__(self, db: Session):
        self.db = db

    def add(self, category: Category) -> Category:
        try:
            self.db.add(category)
            self.db.flush()
            self.db.refresh(category)
            return category
        except SQLAlchemyError:
            return None
    
    def get(self, category_id: int) -> Category:
        try:
            return self.db.query(Category).filter(Category.id == category_id).first()
        except:
            return None
    
    def list(self) -> List[Category]:
        try:
            return self.db.query(Category).all()
        except:
            return []
    
    def update(self, category: Category) -> Category:
        try:
            self.db.flush()
            self.db.refresh(category)
            return category
        except SQLAlchemyError:
            return None
    
    def delete(self, category: Category) -> bool:
        try:
            self.db.delete(category)
            self.db.flush()
            return True
        except SQLAlchemyError:
            return False

    def paginate(self, page: int = 1, per_page: int = 10) -> List[Category]:
        try:
            offset_value = (page - 1) * per_page
            return (
                self.db.query(Category)
                .offset(offset_value)
                .limit(per_page)
                .all()
            )
        except:
            return []
