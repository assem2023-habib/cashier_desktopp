from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List, Dict
from datetime import date, datetime

from models.invoice import Invoice
from models.invoice_item import InvoiceItem
from models.product import Product

from core.repositories.invoice_repository import InvoiceRepository
from core.repositories.invoice_item_repository import InvoiceItemRepository
from core.repositories.product_repository import ProductRepository

class InvoiceService:
    def __init__(self, db: Session):
        self.db= db
        self.invoice_repo= InvoiceRepository(db)
        self.invoice_item_repo= InvoiceItemRepository(db)
        self.product_repo= ProductRepository(db)

    def create_invoice(
            self,
            products: list[Dict]
    )->Optional[Invoice]:
        try:
            validated_products= []
            for item in products:
                product= self.product_repo.get(item['product_id'])

                if not product:
                    raise ValueError(f"Product with id {item['product_id']} not found")
                
                if product.quantity < item['quantity']:
                    raise ValueError(
                        f"Not enough stock for {product.name}. "
                        f"Available: {product.quantity}, Requested: {item['quantity']}"
                    )
                
                validated_products.append({
                    'product': product,
                    'quantity': item['quantity']
                })

            invoice= Invoice(
                customer_id= None,
                date= datetime.now(),
                total_amount=0,
            )

            invoice = self.invoice_repo.add(invoice)

            total= 0

            for item in validated_products:
                product= item['product']
                quantity= item['quantity']

                total_price= product.price * quantity
                total+= total_price

                invoice_item= InvoiceItem(
                    invoice_id= invoice.id,
                    product_id= product.id,
                    quantity= quantity,
                    unit_price= product.price,
                    total_price= total_price
                )

                self.invoice_item_repo.add(invoice_item)

                product.quantity -= quantity
                self.product_repo.update(product)

            invoice.total_amount= total
            self.invoice_repo.update(invoice)

            self.db.commit()
            return invoice
        
        except (SQLAlchemyError, ValueError) as e:
            self.db.rollback()
            return None
        
    def get_invoice_with_details(self, invoice_id: int)->Optional[Dict]:
        try:
            invoice= self.invoice_repo.get(invoice_id)
            if not invoice:
                return None
            
            item= self.invoice_item_repo.list_by_invoice_id(invoice_id)
            customer= None

            return {
                "invoice": invoice,
                "items": item,
                "total_items": len(item)
            }
        except Exception as e:
            return None
        
    def cancel_invoice(self, invoice_id: int)->bool:
        try:
            invoice= self.invoice_repo.get(invoice_id)
            if not invoice:
                return False
            
            items= self.invoice_item_repo.list_by_invoice_id(invoice_id)

            for item in items:
                product= self.product_repo.get(item.product_id)
                if product:
                    product.quantity += item.quantity
                    self.product_repo.update(product)
            
            result= self.invoice_repo.delete(invoice)
            self.db.commit()
            return result
        
        except Exception as e:
            self.db.rollback()
            return False
        
    def calculate_invoice_total(self, invoice_id: int)->int:
        try:
            items= self.invoice_item_repo.list_by_invoice_id(invoice_id)
            return sum(item.total_price for item in items)
        except:
            return 0
        
    def get_invoices_by_date_range(self, start: date, end: date)->List[Invoice]:
        return self.invoice_repo.list_by_date_range(start, end)
    
    def get_invoices_paginated(self, page: int, per_page: int) -> tuple[List[Invoice], int]:
        """Returns a tuple of (invoices, total_count)"""
        try:
            invoices = self.invoice_repo.paginate(page, per_page)
            total_count = self.db.query(Invoice).count()
            return invoices, total_count
        except SQLAlchemyError:
            return [], 0

    def search_invoices(self, query: str) -> List[Invoice]:
        try:
            # Search by ID (as string) or maybe date string if needed
            # For now, simple ID search
            if query.isdigit():
                invoice = self.invoice_repo.get(int(query))
                return [invoice] if invoice else []
            return []
        except SQLAlchemyError:
            return []
    
    def get_today_invoices(self):
        today= date.today()
        return self.invoice_repo.list_by_date_range(today, today)