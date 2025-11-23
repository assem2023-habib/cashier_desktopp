from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QMessageBox

from viewmodels.auth.create_account_viewmodel import CreateAccountViewModel

# Components
from views.components.labels import TitleLabel, SubtitleLabel
from views.components.input_field import InputField
from views.components.password_field import PasswordField
from views.components.primary_button import PrimaryButton

class CreateAccountView(QMainWindow):
    def __init__(self, viewModel: CreateAccountViewModel):
        super().__init__()
        self.vm= viewModel
        self.setWindowTitle("Create Account")
        self.setMinimumSize(400, 500)

        self._build_ui()
        self._bind_viewmodel()

    def _build_ui(self):
        central= QWidget()
        self.setCentralWidget(central)

        layout= QVBoxLayout(central)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(18)

        title= TitleLabel("Create Account")
        subtitle= SubtitleLabel("Create a new user account")
        layout.addWidget(title)
        layout.addWidget(subtitle)

        self.username_input= InputField("Username", icon="👤")
        self.password_input= PasswordField("Password")
        self.confirm_input= PasswordField("Confirm Password")
        
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.confirm_input)

        self.btn_create= PrimaryButton("Create Account", fixed_size= None)
        self.btn_login= PrimaryButton(
            "Already have an account? Login",
            color= "transparent",
            text_color="#2F3C64",
            hover_color="#F5F5F5",
            fixed_size=None
        )

        layout.addWidget(self.btn_create)
        layout.addWidget(self.btn_login)

    def _bind_viewmodel(self):
        self.username_input.textChanged(self.vm.set_username)
        self.password_input.textChanged(self.vm.set_password)
        self.confirm_input.textChanged(self.vm.set_confirmed_password)

        self.btn_create.clicked.connect(self.vm.createCommand)
        self.btn_login.clicked.connect(self.vm.loginCommand)

        self.vm.createAccountRequested.connect(self._go_to_login)
        self.vm.errorChanged.connect(lambda msg: QMessageBox.warning(self, "Error", msg) if msg else None)
        self.vm.successChanged.connect(lambda msg: QMessageBox.information(self, "Success", msg) if msg else None)

        self.vm.togglePasswordVisibilityRequested.connect(
            lambda state: self.confirm_input.input.setEchoMode(
                self.confirm_input.input.Normal if state else self.confirm_input.input.Password
            )
        )
    
    def _go_to_login(self):
        print("Navigate to Login screen")