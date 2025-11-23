from sqlalchemy.orm import Session
from models.invoice import Invoice
from sqlalchemy.exc import SQLAlchemyError
from datetime import date

from core.abstracts.invoice_repository import IInvoiceRepository

class InvoiceRepository(IInvoiceRepository):
    def __init__(self, db: Session):
        self.db= db

    def add(self, invoice: Invoice)->Invoice:
        try:
            self.db.add(invoice)
            self.db.flush()  
            self.db.refresh(invoice)
            return invoice
        except SQLAlchemyError:
            return None
    
    def get(self, invoice_id: int)->Invoice:
        try:
            return self.db.query(Invoice).filter(Invoice.id == invoice_id).first()
        except:
            return None
    
    def list(self)->list[Invoice]:
        try:
            return self.db.query(Invoice).all()
        except:
            return []
    
    def update(self, invoice: Invoice)->Invoice:
        try:
            self.db.flush()
            self.db.refresh(invoice)
            return invoice
        except SQLAlchemyError:
            return None
    
    def delete(self, invoice: Invoice)->None:
        try:
            self.db.delete(invoice)
            self.db.flush()
            return True
        except SQLAlchemyError:
            return False

    def list_by_date_range(self, start: date, end: date)->list[Invoice]:
        try:
            return (
                self.db.query(Invoice)
                .filter(Invoice.date.between(start, end))
                .all()
            )
        except:
            return []
    
    def paginate(self, page: int, per_page: int)->list[Invoice]:
        try:
            offset_value = (page - 1) * per_page
            return (
                self.db.query(Invoice)
                .offset(offset_value)
                .limit(per_page)
                .all()
            )
        except:
            return []
    
    