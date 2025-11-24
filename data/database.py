from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
import os

BASE_DIR= os.path.dirname(os.path.abspath(__file__))
DB_PATH= os.path.join(BASE_DIR, "cashier.db")

DATABASE_URL= f"sqlite:///{DB_PATH}"

engine= create_engine(
    DATABASE_URL,
    echo= False,
    connect_args= {"check_same_thread": False}
)

SessionLocal= sessionmaker(
    autocommit= False,
    autoflush= False,
    bind= engine
)

def get_session():
    session= SessionLocal()
    try:
        yield session

    finally:
        session.close()

def init_db():
    from models.user import User
    from models.product import Product
    from models.category import Category
    from models.invoice import Invoice
    from models.invoice_item import InvoiceItem
    from models.customer import Customer

    Base.metadata.create_all(bind= engine)
    print("✔ Database tables created successfully!")