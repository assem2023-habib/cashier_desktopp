from sqlalchemy.orm import Session
from models.invoice_item import InvoiceItem
from core.abstracts.invoice_item_repository import IInvoiceItemRepository

class InvoiceItemRepository(IInvoiceItemRepository):
    def __init__(self, db: Session):
        self.db= db

    def add(self, item: InvoiceItem)->InvoiceItem:
        self.db.add(item)
        self.db.flush()
        self.db.refresh(item)
        return item
    
    def get(self, item_id: int)->InvoiceItem:
        return self.db.query(InvoiceItem).filter(InvoiceItem.id == item_id).first()
    
    def list(self)->list[InvoiceItem]:
        return self.db.query(InvoiceItem).all()
    
    def update(self, item: InvoiceItem)->InvoiceItem:
        self.db.flush()
        self.db.refresh(item)
        return item
    
    def delete(self, item: InvoiceItem)->None:
        try:
            self.db.delete(item)
            self.db.flush()
            return True
        except:
            return False

    def list_by_invoice_id(self, invoice_id: int)->list[InvoiceItem]:
        return self.db.query(InvoiceItem).filter(InvoiceItem.invoice_id == invoice_id).all()
    
    def paginate(self, page: int, per_page: int)->list[InvoiceItem]:
        offset_value= (page - 1) * per_page
        return self.db.query(InvoiceItem).offset(offset_value).limit(per_page).all()