from sqlalchemy.orm import Session
from models.product import Product
from sqlalchemy.exc import SQLAlchemyError

from core.abstracts.product_repository import IProductRepository

class ProductRepository(IProductRepository):
    def __init__(self, db:Session):
        self.db= db

    def add(self, product: Product)->Product:
        try:
            self.db.add(product)
            self.db.flush()
            self.db.refresh(product)
            return product
        except SQLAlchemyError:
            return None
    
    def get(self, product_id: int)->Product:
        try:
            return self.db.query(Product).filter(Product.id == product_id).first()
        except:
            return None
    
    def list(self)->list[Product]:
        try:
            return self.db.query(Product).all()
        except:
            return []
    
    def update(self, product: Product)->Product:
        try:
            self.db.flush()
            self.db.refresh(product)
            return product
        except SQLAlchemyError:
            return None
    
    def delete(self, product:Product)->None:
        try:
            self.db.delete(product)
            self.db.flush()
            return True
        except SQLAlchemyError:
            return False

    def get_by_barcode(self, barcode: str)->Product:
        try:
            return (
                self.db.query(Product)
                .filter(Product.barcode == barcode)
                .first()
            )
        except:
            return None
    
    def paginate(self, page: int, per_page: int)->list[Product]:
        try:
            offset_value = (page - 1) * per_page
            return (
                self.db.query(Product)
                .offset(offset_value)
                .limit(per_page)
                .all()
            )
        except:
            return []