from PySide6.QtCore import QObject, Signal, Slot, Property
from core.services.user_service import UserService
from sqlalchemy.orm import Session

class CreateAccountViewModel(QObject):
    usernameChanged= Signal(str)
    passwordChanged= Signal(str)
    confirmPasswordChanged= Signal(str)

    isLoadingChanged= Signal(bool)
    errorChanged= Signal(str)
    successChanged = Signal(str)

    createAccountRequested= Signal()
    goTologinRequested= Signal()
    togglePasswordVisibilityRequested= Signal(bool)

    def __init__(self, db_session):
        super().__init__()

        self._username= ""
        self._password= ""
        self._confirm_password= ""

        self._is_loading= False
        self._error= ""
        self._success= ""
        self.user_service= UserService(db_session)

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

    password= Property(str, get_password, set_password, notify=passwordChanged)

    def get_confirmed_password(self):
        return self._confirm_password

    def set_confirmed_password(self, value):
        if self._confirm_password != value:
            self._confirm_password= value
            self.confirmPasswordChanged.emit(value)

    confirmPassword= Property(str, get_confirmed_password, set_confirmed_password, notify=confirmPasswordChanged)

    def get_loading(self):
        return self._is_loading

    def set_loading(self, value):
        if self._is_loading != value:
            self._is_loading= value
            self.isLoadingChanged.emit(value)

    isLoading= Property(bool, get_loading, set_loading, notify=isLoadingChanged)

    def get_error(self):
        return self._error

    def set_error(self, value):
        if self._error != value:
            self._error = value
            self.errorChanged.emit(value)

    error = Property(str, get_error, set_error, notify=errorChanged)

    def get_success(self): 
        return self._success

    def set_success(self, value):
        if self._success != value:
            self._success = value
            self.successChanged.emit(value)

    success = Property(str, get_success, set_success, notify=successChanged)

    @Slot()
    def createCommand(self):
        if self._password != self._confirm_password:
            self.set_error("Passwords do not match.")
            return
        
        if len(self._username) < 3:
            self.set_error("Username must be at least 3 characters.")
            return

        if len(self._password) < 6:
            self.set_error("Password must be at least 6 characters.")
            return
        self.set_loading(True)
        user= self.user_service.create_user(
            user_name=self._username,
            password=self._password
        )
        self.set_loading(False)

        if user:
            self.set_success("Account created successfully!")
            self.createAccountRequested.emit()
        else:
            self.set_error("Failed to create account. Username may exist.")

    @Slot()
    def loginCommand(self):
        self.goTologinRequested.emit()

    @Slot(bool)
    def togglePasswordVisibilityCommand(self, state):
        self.togglePasswordVisibilityRequested.emit(state)
