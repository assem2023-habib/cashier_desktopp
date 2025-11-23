from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from models.base import Base
from sqlalchemy.types import Enum as SQLEnum
from enums.invoice_status_enum import InvoiceStatus

class Invoice(Base):
    __tablename__= "invoices"

    id= Column(Integer, primary_key= True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True)
    date= Column(DateTime, default= datetime.now)
    status= Column(SQLEnum(InvoiceStatus), default= InvoiceStatus.PENDING)
    total_amount= Column(Integer, default= 0)

    customer = relationship("Customer", back_populates="invoices")
    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete")

    def __repr__(self):
        return f"<Invoice(id={self.id}, total= {self.total_amount})>"