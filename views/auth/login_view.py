from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QGraphicsDropShadowEffect, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from viewmodels.auth.login_viewmodel import LoginViewModel

# Components
from views.components.input_field import InputField
from views.components.password_field import PasswordField
from views.components.card_widget import CardWidget

from views.auth.create_account_view import CreateAccountView
from viewmodels.auth.create_account_viewmodel import CreateAccountViewModel
from data.database import SessionLocal

class LoginView(QMainWindow):
    def __init__(self, viewModel: LoginViewModel):
        super().__init__()
        self.vm = viewModel

        self.setWindowTitle("Login")
        self.setStyleSheet("QMainWindow { background-color: #3C4753; }")
        self.setMinimumSize(900, 700)

        self._build_ui()
        self._bind_viewmodel()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        
        # Center the card
        main_layout = QVBoxLayout(central)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Main Form Container (Card)
        self.card = CardWidget()
        self.card.setFixedWidth(450)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect(self.card)
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(8)
        shadow.setColor(QColor(0, 0, 0, 51))
        self.card.setGraphicsEffect(shadow)

        # Form Layout
        form_layout = self.card.layout
        form_layout.setContentsMargins(40, 40, 40, 40)
        form_layout.setSpacing(20)

        # Header
        title = QLabel("Login to Your Account")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-family: Sans-serif;
                font-weight: bold;
                font-size: 26px;
                color: #333333;
            }
        """)
        form_layout.addWidget(title)
        
        # Input Fields
        self.username_input = InputField("Enter your username")
        self.password_input = PasswordField("Enter your password")
        
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_input)

        # Error Message
        self.lbl_error = QLabel("Invalid credentials")
        self.lbl_error.setStyleSheet("""
            QLabel {
                font-family: Sans-serif;
                font-size: 13px;
                color: #DC3545;
            }
        """)
        self.lbl_error.hide()
        form_layout.addWidget(self.lbl_error)

        # Remember Me Checkbox
        self.chk_remember = QCheckBox("Remember me")
        self.chk_remember.setCursor(Qt.PointingHandCursor)
        self.chk_remember.setStyleSheet("""
            QCheckBox {
                font-family: Sans-serif;
                font-size: 14px;
                color: #333333;
                spacing: 8px;
            }
        """)
        form_layout.addWidget(self.chk_remember)

        # Login Button
        self.btn_login = QPushButton("Login")
        self.btn_login.setCursor(Qt.PointingHandCursor)
        self.btn_login.setFixedHeight(44)
        self.btn_login.setStyleSheet("""
            QPushButton {
                background-color: #4C95ED;
                color: white;
                font-family: Sans-serif;
                font-weight: bold;
                font-size: 16px;
                border-radius: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #3B82F6;
            }
            QPushButton:pressed {
                background-color: #2563EB;
            }
        """)
        form_layout.addWidget(self.btn_login)

        # Footer
        footer_layout = QHBoxLayout()
        footer_layout.setAlignment(Qt.AlignCenter)
        footer_layout.setSpacing(4)
        
        lbl_dont_have = QLabel("Don't have an account?")
        lbl_dont_have.setStyleSheet("font-family: Sans-serif; font-size: 14px; color: #333333;")
        
        self.btn_create_link = QPushButton("Create one")
        self.btn_create_link.setCursor(Qt.PointingHandCursor)
        self.btn_create_link.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #4C95ED;
                font-family: Sans-serif;
                font-size: 14px;
                text-decoration: underline;
                border: none;
                padding: 0;
            }
            QPushButton:hover {
                color: #3B82F6;
            }
        """)
        
        footer_layout.addWidget(lbl_dont_have)
        footer_layout.addWidget(self.btn_create_link)
        form_layout.addLayout(footer_layout)
        
        main_layout.addWidget(self.card)

    def _bind_viewmodel(self):
        self.username_input.textChanged(self.vm.set_username)
        self.password_input.textChanged(self.vm.set_password)

        # Bind Remember Me
        self.chk_remember.toggled.connect(self.vm.set_remember_me)
        self.chk_remember.setChecked(self.vm.rememberMe)
        
        # If credentials loaded, update inputs
        if self.vm.rememberMe:
            self.username_input.setText(self.vm.username)
            self.password_input.setText(self.vm.password)

        self.btn_login.clicked.connect(self.vm.loginCommand)
        self.btn_create_link.clicked.connect(self.vm.goToRegisterCommand)

        self.vm.loginRequest.connect(self._go_to_dashboard)
        self.vm.errorChanged.connect(self._on_error)
        self.vm.goToRegisterRequest.connect(self._go_to_create_account)

    def _on_error(self, message):
        if message:
            self.lbl_error.setText(message)
            self.lbl_error.show()
        else:
            self.lbl_error.hide()

    def _go_to_create_account(self):
        db_session = SessionLocal()
        create_vm = CreateAccountViewModel(db_session)
        self.create_account_window = CreateAccountView(create_vm)
        self.create_account_window.show()
        self.close()

    def _go_to_dashboard(self):
        from views.dashboard.dashboard_view import DashboardView
        from viewmodels.dashboard.dashboard_viewmodel import DashboardViewModel
        
        dashboard_vm = DashboardViewModel(db_session=self.vm.db_session, current_user=self.vm.logged_user)
        self.dashboard_window = DashboardView(dashboard_vm)
        self.dashboard_window.show()
        self.close()