from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from PySide6.QtCore import Qt

from viewmodels.auth.login_viewmodel import LoginViewModel

# Components
from views.components.labels import TitleLabel, SubtitleLabel
from views.components.input_field import InputField
from views.components.password_field import PasswordField
from views.components.primary_button import PrimaryButton

from views.auth.create_account_view import CreateAccountView
from viewmodels.auth.create_account_viewmodel import CreateAccountViewModel
from data.database import SessionLocal

class LoginView(QMainWindow):
    def __init__(self, viewModel: LoginViewModel):
        super().__init__()
        self.vm= viewModel

        self.setWindowTitle("Login")
        self.setMinimumSize(400, 420)

        self._build_ui()
        self._bind_viewmodel()


    def _build_ui(self):
        central= QWidget()
        self.setCentralWidget(central)

        layout= QVBoxLayout(central)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(18)

        layout.addWidget(TitleLabel("Welcom Back"))
        layout.addWidget(SubtitleLabel("Login to your account"))

        self.username_input= InputField("Username", icon="👤")
        self.password_input= PasswordField("Password")

        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)

        self.btn_login= PrimaryButton("Login", fixed_size= None)

        self.btn_create_account= PrimaryButton(
            "Don't have an account? Register",
            color="#FFFFFF",
            text_color="#2F3C64",
            hover_color="#F5F5F5",
            fixed_size=None
        )

        layout.addWidget(self.btn_login)
        layout.addWidget(self.btn_create_account)

    def _bind_viewmodel(self):
        self.username_input.textChanged(self.vm.set_username)
        self.password_input.textChanged(self.vm.set_password)

        self.btn_login.clicked.connect(self.vm.loginCommand)
        self.btn_create_account.clicked.connect(self.vm.goToRegisterCommand)

        self.vm.errorChanged.connect(self._on_error)
        self.vm.goToRegisterRequest.connect(self._go_to_create_account)

    def _on_error(self, message):
        print("Login error", message)

    def _go_to_create_account(self):
        db_session= SessionLocal()
        create_vm= CreateAccountViewModel(db_session)
        self.create_account_window = CreateAccountView(db_session)
        self.create_account_window.show()
        self.close()