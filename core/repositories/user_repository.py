from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import bcrypt # type: ignore
from typing import List

from models.user import User
from core.abstracts.user_repository import IUserRepository

class UserRepository(IUserRepository):
    def __init__(self, db:Session):
        self.db = db

    def add(self, user: User)->User:
        try:
            if user._password:
                user.set_password(user._password)
            else:
                raise ValueError("Password is required for new user")

            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user

        except Exception as e:
            self.db.rollback()
            return None
    
    def get(self, user_id: int)->User:
        return self.db.query(User).filter(User.id == user_id).first()
    
    def list(self)-> list[User]:
        return self.db.query(User).all()
    
    def update(self, user: User)->User:
        try:
            if user._password:
                user.set_password(user._password)
            self.db.commit()
            self.db.refresh(user)
            return user
        except SQLAlchemyError as e:
            self.db.rollback()
            return None
    
    def delete(self, user: User)->bool:
        try:
            self.db.delete(user)
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False

    def get_by_username(self, user_name: str)->User:
        return self.db.query(User).filter(User.user_name == user_name).first()
    
    def authenticate(self, user_name: str, password: str)->User:
        user= self.get_by_username(user_name= user_name)
        if user and user.check_password(password):
            return user
        return None
    
    def  paginate(self, page:int, per_page: int)->List[User]:
        try:
            if page < 1 or per_page < 1:
                return []
            offset_value= (page - 1) * per_page
            return self.db.query(User).offset(offset_value).limit(per_page).all()
        except SQLAlchemyError:
            return []

        