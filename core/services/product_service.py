from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List
from models.product import Product
from core.repositories.product_repository import ProductRepository

class ProductService:
    def __init__(self, db:Session):
        self.db = db
        self.product_repo = ProductRepository(db)

    def create_product(
            self,
            name: str,
            barcode: str,
            price: int,
            quantity: int
    )->Optional[Product]:
        try:
            if price <= 0:
                raise ValueError("Price must be greater than 0")
            
            if quantity < 0:
                raise ValueError("Stock cannot be negative")
            
            existing= self.product_repo.get_by_barcode(barcode)
            if existing:
                raise ValueError(f"Product with barcode {barcode} already exists")
            
            product= Product(
                name= name,
                barcode= barcode,
                price= price,
                quantity= quantity,
            )

            product = self.product_repo.add(product)
            self.db.commit()
            return product
        
        except (SQLAlchemyError, ValueError) as e:
            self.db.rollback()
            return None
        
    def update_quantity(
        self,
        product_id: int,
        quantity: int,
        operation: str = "add",
    )-> Optional[Product]:
        try:
            product= self.product_repo.get(product_id)
            if not product:
                raise ValueError(f"Product {product_id} not found")
            
            if operation == "add":
                product.quantity += quantity

            elif operation == "sub":
                if product.quantity < quantity:
                    raise ValueError(
                        f"Not enough stock. Available: {product.quantity}, "
                        f"Requested: {quantity}"
                    )
                product.quantity -= quantity

            else:
                raise ValueError(f"Invalid operation: {operation}")
            
            product = self.product_repo.update(product)
            self.db.commit()
            return product
        
        except (SQLAlchemyError, ValueError) as e:
            self.db.rollback()
            return None
        
    def get_low_quantity_products(self, threshold: int= 10)->list[Product]:
        try:
            all_proudcts= self.product_repo.list()
            return [p for p in all_proudcts if p.quantity <= threshold]
        except SQLAlchemyError:
            return []
        
    def search_products(self, query: str)->list[Product]:
        try:
            all_products= self.product_repo.list()
            query_lower = query.lower()
            return [
                p for p in all_products 
                if query_lower in p.name.lower() or query_lower in p.barcode
            ]
        
        except SQLAlchemyError:
            return []
        
    def get_product_by_barcode(self, barcode: str)->Optional[Product]:
        return self.product_repo.get_by_barcode(barcode)
    
    def update_price(self, product_id: int, new_price:int)->Optional[Product]:
        try:
            if new_price <= 0:
                raise ValueError("Price must be greater than 0")
            
            product= self.product_repo.get(product_id)

            if not product:
                raise ValueError(f"Product {product_id} not found")
            
            product.price= new_price
            product = self.product_repo.update(product)
            self.db.commit()

            return product
        
        except(SQLAlchemyError, ValueError) as e:
            self.db.rollback()
            return None