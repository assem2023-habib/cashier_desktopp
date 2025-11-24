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
            quantity: int,
            category_id: Optional[int] = None
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
                category_id= category_id
            )

            product = self.product_repo.add(product)
            self.db.commit()
            return product
        
        except (SQLAlchemyError, ValueError) as e:
            self.db.rollback()
            raise
        
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
            raise
        
    def get_low_quantity_products(self, threshold: int= 10)->List[Product]:
        try:
            all_proudcts= self.product_repo.list()
            return [p for p in all_proudcts if p.quantity <= threshold]
        except SQLAlchemyError:
            return []
        
    def search_products(self, query: str)->List[Product]:
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
    
    def update_product(
        self,
        product_id: int,
        name: str,
        barcode: str,
        price: int,
        quantity: int,
        category_id: Optional[int] = None
    ) -> Optional[Product]:
        try:
            product = self.product_repo.get(product_id)
            if not product:
                raise ValueError(f"Product {product_id} not found")

            # Check if barcode is being changed to one that already exists
            if barcode != product.barcode:
                existing = self.product_repo.get_by_barcode(barcode)
                if existing:
                    raise ValueError(f"Product with barcode {barcode} already exists")

            product.name = name
            product.barcode = barcode
            product.price = price
            product.quantity = quantity
            product.category_id = category_id

            product = self.product_repo.update(product)
            self.db.commit()
            return product
        except (SQLAlchemyError, ValueError) as e:
            self.db.rollback()
            raise

    def delete_product(self, product_id: int) -> bool:
        try:
            product = self.product_repo.get(product_id)
            if not product:
                raise ValueError("Product not found")
            
            success = self.product_repo.delete(product)
            if success:
                self.db.commit()
                return True
            return False
        except (SQLAlchemyError, ValueError) as e:
            self.db.rollback()
            raise

    def get_products_paginated(self, page: int, per_page: int) -> tuple[List[Product], int]:
        """Returns a tuple of (products, total_count)"""
        try:
            products = self.product_repo.paginate(page, per_page)
            # We need a count method in repo ideally, but for now let's just get all count
            # This is inefficient for large datasets but works for now. 
            # Ideally repo should have count().
            # Let's add a quick count query here or just list() len if repo doesn't support count.
            # Checking repo... it has list().
            total_count = self.db.query(Product).count()
            return products, total_count
        except SQLAlchemyError:
            return [], 0

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
            raise