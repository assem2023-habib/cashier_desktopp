from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class InvoiceItem(Base):
    __tablename__= "invoice_items"

    id= Column(Integer, primary_key= True)
    invoice_id= Column(Integer, ForeignKey("invoices.id"))
    product_id= Column(Integer, ForeignKey("products.id"))
    quantity= Column(Integer, nullable= False)
    unit_price= Column(Integer, nullable= False)
    total_price= Column(Integer, nullable= False)

    product = relationship("Product", back_populates="items")
    invoice = relationship("Invoice", back_populates="items")
    def __repr__(self):
        return (
            f"<InvoiceItem(product_id={self.product_id}, "
            f"quantity={self.quantity}, total={self.total_price})>"
        )