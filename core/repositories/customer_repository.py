from sqlalchemy.orm import Session
from models.customer import Customer
from core.abstracts.customer_repository import ICustomerRepository

class CustomerRepository(ICustomerRepository):
    def __init__(self, db: Session):
        self.db= db

    def add(self, customer: Customer)->Customer:
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        return customer
    
    def get(self, customer_id: int)-> Customer:
        return self.db.query(Customer).filter(Customer.id == customer_id).first()
    
    def list(self)->list[Customer]:
        return self.db.query(Customer).all()
    
    def update(self, customer: Customer)->Customer:
        self.db.commit()
        self.db.refresh(customer)
        return customer
    
    def delete(self, customer: Customer)->None:
        try:
            self.db.delete(customer)
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False


    def get_by_name(self, name: str) -> Customer:
        return self.db.query(Customer).filter(Customer.name == name).first()

    def get_by_phone(self, phone: str) -> Customer:
        return self.db.query(Customer).filter(Customer.phone == phone).first()
    
    def paginate(self, page: int, per_page: int)->list[Customer]:
        offset_value= (page - 1) * per_page
        return self.db.query(Customer).offset(offset_value).limit(per_page).all()