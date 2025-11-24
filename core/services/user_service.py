from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional, List
from models.user import User
from enums.user_role_enum import UserRole
from core.repositories.user_repository import UserRepository

class UserService:
    def __init__(self, db:Session):
        self.db= db
        self.user_repo= UserRepository(db)

    def create_user(
            self,
            user_name: str,
            password: str,
            role: UserRole = UserRole.EMPLOYEE
    )->Optional[User]:
        try:
            if len(user_name) < 3:
                raise ValueError("Username must be at least 3 chararcters")
            if len(password) < 6:
                raise ValueError("Password must be at least 6 characters")
            
            existing= self.user_repo.get_by_username(user_name)
            if existing:
                raise ValueError(f"Username {user_name} already exists")
            
            user= User(
                user_name= user_name,
                role= role
            )
            user._password= password
            return self.user_repo.add(user= user)
        
        except (SQLAlchemyError, ValueError) as e:
            self.db.rollback()
            print(f"Error creating user: {e}")
            return None
        
    def login(self, user_name:str, password: str)->Optional[User]:
        return self.user_repo.authenticate(user_name, password)
    
    def change_password(
            self,
            user_id: int,
            old_password: str,
            new_password: str,
    )->bool:
        try:
            user= self.user_repo.get(user_id)
            if not user:
                raise ValueError("User not Found")
            
            if not user.check_password(old_password):
                raise ValueError("Invalid old password")

            if len(new_password) < 6:
                raise ValueError("New password must be at least 6 characters")
            
            user.password= new_password
            self.user_repo.update(user)
            return True
        except (SQLAlchemyError, ValueError) as e:
            self.db.rollback()
            return False
        
    def update_user_role(self, user_id: int, new_role: UserRole)->Optional[User]:
        try:
            user= self.user_repo.get(user_id)
            if not user:
                raise ValueError("User not found")
            
            user.role= new_role
            return self.user_repo.update(user)
        
        except (SQLAlchemyError, ValueError) as e:
            self.db.rollback()
            return None
        
    def get_all_user(self)->List[User]:
        return self.user_repo.list()
    
    def check_permission(self, user: User, requried_role: UserRole)->bool:
        if user.role == UserRole.ADMIN:
            return True
        return user.role == requried_role

    def get_users_paginated(self, page: int, per_page: int) -> tuple[List[User], int]:
        """Returns a tuple of (users, total_count)"""
        try:
            users = self.user_repo.paginate(page, per_page)
            # Ideally repo should have count(), using len(all) for now or query count
            total_count = self.db.query(User).count()
            return users, total_count
        except SQLAlchemyError:
            return [], 0

    def update_user(self, user_id: int, user_name: str, role: UserRole, password: str = None) -> Optional[User]:
        try:
            user = self.user_repo.get(user_id)
            if not user:
                raise ValueError("User not found")
            
            # Check if username is being changed to one that already exists
            if user_name != user.user_name:
                existing = self.user_repo.get_by_username(user_name)
                if existing:
                    raise ValueError(f"Username {user_name} already exists")
            
            user.user_name = user_name
            user.role = role
            
            if password:
                if len(password) < 6:
                    raise ValueError("Password must be at least 6 characters")
                user.set_password(password)
            
            return self.user_repo.update(user)
        except (SQLAlchemyError, ValueError) as e:
            self.db.rollback()
            return None

    def delete_user(self, user_id: int) -> bool:
        try:
            user = self.user_repo.get(user_id)
            if not user:
                return False
            return self.user_repo.delete(user)
        except SQLAlchemyError:
            self.db.rollback()
            return False