from PySide6.QtCore import QObject, Signal, Slot, Property, QSettings
from sqlalchemy.orm import Session

from core.services.user_service import UserService
from enums.user_role_enum import UserRole

class LoginViewModel(QObject):

    usernameChanged= Signal(str)
    passwordChanged= Signal(str)

    errorChanged= Signal(str)

    loginRequest= Signal()
    goToRegisterRequest= Signal()

    rememberMeChanged = Signal(bool)
    def __init__(self, db_session: Session):
        super().__init__()

        self._username= ""
        self._password= ""
        self._error= ""
        self._remember_me = False
        self.db_session = db_session
        self.user_serivce= UserService(db_session)
        self.logged_user = None  # Store logged-in user
        
        self._load_credentials()

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

    def get_remember_me(self):
        return self._remember_me

    def set_remember_me(self, value):
        if self._remember_me != value:
            self._remember_me = value
            self.rememberMeChanged.emit(value)

    rememberMe = Property(bool, get_remember_me, set_remember_me, notify=rememberMeChanged)

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
            self.logged_user = user  # Store the logged-in user
            print(f"Logged in as {user.user_name} ({user.role})")
            
            if self._remember_me:
                self._save_credentials()
            else:
                self._clear_credentials()
                
            self.loginRequest.emit()
        else:
            self.set_error("Invalid username or password")

    @Slot()
    def goToRegisterCommand(self):
        self.goToRegisterRequest.emit()

    def _save_credentials(self):
        settings = QSettings("MyCompany", "CashierApp")
        settings.setValue("username", self._username)
        settings.setValue("password", self._password) # Note: In production, encrypt this!
        settings.setValue("remember_me", True)

    def _load_credentials(self):
        settings = QSettings("MyCompany", "CashierApp")
        if settings.value("remember_me", False, type=bool):
            self.set_username(settings.value("username", ""))
            self.set_password(settings.value("password", ""))
            self.set_remember_me(True)

    def _clear_credentials(self):
        settings = QSettings("MyCompany", "CashierApp")
        settings.remove("username")
        settings.remove("password")
        settings.setValue("remember_me", False)