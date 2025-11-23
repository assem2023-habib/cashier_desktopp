from sqlalchemy import Column, Integer, String
from models.base import Base
from passlib.hash import bcrypt # type: ignore
from sqlalchemy.types import Enum as SQLEnum
from enums.user_role_enum import UserRole

class User(Base):
    __tablename__= "users"

    id= Column(Integer, primary_key= True)
    user_name= Column(String(50), unique=True, nullable= False)
    password_hash= Column(String(255), nullable= False)
    role= Column(SQLEnum(UserRole), default=UserRole.EMPLOYEE)

    _password = None
    
    @property
    def password(self):
        raise AttributeError("Password is not readable")
    
    @password.setter
    def password(self, value: str):
        self._password = value

    def set_password(self, password: str):
        """تشفير كلمة المرور وحفظها"""
        self.password_hash = bcrypt.hash(password)
        self._password = None  # تنظيف بعد التشفير



    def check_password(self, password):
        return bcrypt.verify(password, self.password_hash)
    
    def __repr__(self):
        return f"<User(user_name={self.user_name}, role={self.role})"