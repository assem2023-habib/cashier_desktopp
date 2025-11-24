from sqlalchemy import Column, Integer, String, Float, ForeignKey
from models.base import Base
from sqlalchemy.orm import relationship
    
class Product(Base):
    __tablename__= "products"

    id = Column(Integer, primary_key= True)
    name= Column(String(100), nullable= False)
    price= Column(Integer, nullable= False)
    quantity= Column(Integer, default= 0)
    barcode= Column(String(50), unique= True, nullable= True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    category = relationship("Category", back_populates="products")
    items = relationship("InvoiceItem", back_populates="product")

    def __repr__(self):
        return f"<Product(name={self.name}, price={self.price})>"