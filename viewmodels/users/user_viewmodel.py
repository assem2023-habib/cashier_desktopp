from PySide6.QtCore import QObject, Signal, Slot, Property
from typing import List, Optional
from core.services.user_service import UserService
from models.user import User
from enums.user_role_enum import UserRole
from sqlalchemy.orm import Session
import math

class UserViewModel(QObject):
    usersChanged = Signal()
    paginationChanged = Signal()
    isLoadingChanged = Signal(bool)
    errorChanged = Signal(str)
    successChanged = Signal(str)

    def __init__(self, db_session: Session):
        super().__init__()
        self.db_session = db_session
        self.user_service = UserService(db_session)
        
        self._users = []
        self._current_page = 1
        self._per_page = 10
        self._total_items = 0
        self._total_pages = 0
        self._is_loading = False
        self._error = ""
        self._success = ""

        # Initial load
        self.load_users()

    @Property(bool, notify=isLoadingChanged)
    def isLoading(self):
        return self._is_loading

    @isLoading.setter
    def isLoading(self, value):
        if self._is_loading != value:
            self._is_loading = value
            self.isLoadingChanged.emit(value)

    @Property(str, notify=errorChanged)
    def error(self):
        return self._error
    
    @error.setter
    def error(self, value):
        if self._error != value:
            self._error = value
            self.errorChanged.emit(value)

    @Property(str, notify=successChanged)
    def success(self):
        return self._success
    
    @success.setter
    def success(self, value):
        if self._success != value:
            self._success = value
            self.successChanged.emit(value)

    @Property(int, notify=paginationChanged)
    def currentPage(self):
        return self._current_page

    @Property(int, notify=paginationChanged)
    def totalPages(self):
        return self._total_pages
    
    @Property(int, notify=paginationChanged)
    def totalItems(self):
        return self._total_items

    def get_users(self) -> List[User]:
        return self._users

    @Slot()
    def load_users(self):
        self.isLoading = True
        self.error = ""
        try:
            self._users, self._total_items = self.user_service.get_users_paginated(
                self._current_page, self._per_page
            )
            self._total_pages = math.ceil(self._total_items / self._per_page) if self._total_items > 0 else 1
            
            self.usersChanged.emit()
            self.paginationChanged.emit()
            
        except Exception as e:
            self.error = f"Failed to load users: {str(e)}"
        finally:
            self.isLoading = False

    @Slot()
    def nextPage(self):
        if self._current_page < self._total_pages:
            self._current_page += 1
            self.load_users()

    @Slot()
    def prevPage(self):
        if self._current_page > 1:
            self._current_page -= 1
            self.load_users()

    @Slot(str, str, str)
    def addUser(self, username: str, password: str, role_str: str):
        self.isLoading = True
        self.error = ""
        self.success = ""
        try:
            role = UserRole(role_str)
            user = self.user_service.create_user(username, password, role)
            if user:
                self.success = "User created successfully"
                self.load_users()
            else:
                self.error = "Failed to create user"
        except Exception as e:
            self.error = f"Error creating user: {str(e)}"
        finally:
            self.isLoading = False

    @Slot(int, str, str, str)
    def updateUser(self, user_id: int, username: str, role_str: str, password: str = None):
        self.isLoading = True
        self.error = ""
        self.success = ""
        try:
            role = UserRole(role_str)
            # Pass None if password is empty string to avoid changing it
            pwd = password if password else None
            user = self.user_service.update_user(user_id, username, role, pwd)
            if user:
                self.success = "User updated successfully"
                self.load_users()
            else:
                self.error = "Failed to update user"
        except Exception as e:
            self.error = f"Error updating user: {str(e)}"
        finally:
            self.isLoading = False

    @Slot(int)
    def deleteUser(self, user_id: int):
        self.isLoading = True
        self.error = ""
        self.success = ""
        try:
            if self.user_service.delete_user(user_id):
                self.success = "User deleted successfully"
                self.load_users()
            else:
                self.error = "Failed to delete user"
        except Exception as e:
            self.error = f"Error deleting user: {str(e)}"
        finally:
            self.isLoading = False
