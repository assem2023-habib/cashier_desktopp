from PySide6.QtCore import QObject, Signal, Slot, Property
from sqlalchemy.orm import Session

from core.services.user_service import UserService
from enums.user_role_enum import UserRole

class LoginViewModel(QObject):

    usernameChanged= Signal(str)
    passwordChanged= Signal(str)

    errorChanged= Signal(str)

    loginRequest= Signal()
    goToRegisterRequest= Signal()

    def __init__(self, db_session: Session):
        super().__init__()

        self._username= ""
        self._password= ""
        self._error= ""
        self.user_serivce= UserService(db_session)

    def get_username(self):
        return self._username
    
    def set_username(self, value):
        if self._username != value:
            self._username= value
            self.usernameChanged.emit(value)

    username= Property(str, get_username, set_username, notify= usernameChanged)

    def get_password(self):
        return self._password
    
    def set_password(self, value):
        if self._password != value:
            self._password= value
            self.passwordChanged.emit(value)

    password= Property(str, get_password, set_password, notify= passwordChanged)

    def get_error(self):
        return self._error
    
    def set_error(self, value):
        if self._error != value:
            self._error= value
            self.errorChanged.emit(value)

    error= Property(str, get_error, set_error, notify= errorChanged)

    @Slot()
    def loginCommand(self):
        if not self._username or not self._password:
            self.set_error("Username and password cannot be empty")
            return
        user= self.user_serivce.login(self._username, self._password)
        if user:
            self.set_error("")
            print(f"Logged in as {user.user_name} ({user.role})")
            self.loginRequest.emit()
        else:
            self.set_error("Invalid username or password")

    @Slot()
    def goToRegisterCommand(self):
        self.goToRegisterRequest.emit()