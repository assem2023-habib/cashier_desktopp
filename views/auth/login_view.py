from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QGraphicsDropShadowEffect, QSizePolicy, QFrame
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QCursor

from viewmodels.auth.login_viewmodel import LoginViewModel

# Components
from views.components.input_field import InputField
from views.components.password_field import PasswordField
from views.components.primary_button import PrimaryButton
from views.components.card_widget import CardWidget

from views.auth.create_account_view import CreateAccountView
from viewmodels.auth.create_account_viewmodel import CreateAccountViewModel
from data.database import SessionLocal

class LoginView(QMainWindow):
    def __init__(self, viewModel: LoginViewModel):
        super().__init__()
        self.vm = viewModel

        self.setWindowTitle("Login")
        # Main Window Background: Dark Grey #3C4753
        self.setStyleSheet("QMainWindow { background-color: #3C4753; }")
        self.setMinimumSize(900, 700) # Adjusted to show the centered layout well

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
        self.card.setFixedWidth(450) # Medium width (400px to 500px)
        
        # Override Card Style for specific requirements
        # Shape: Rectangular with moderately rounded corners (12px to 18px) -> CardWidget has 18px
        # Color: Pure white -> CardWidget has white
        # Shadow: Prominent, soft, diffused (0px 8px 30px rgba(0, 0, 0, 0.2))
        shadow = QGraphicsDropShadowEffect(self.card)
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(8)
        shadow.setColor(QColor(0, 0, 0, 51)) # 0.2 alpha * 255 = 51
        self.card.setGraphicsEffect(shadow)

        # Form Layout
        form_layout = self.card.layout
        form_layout.setContentsMargins(40, 40, 40, 40) # Consistent padding
        form_layout.setSpacing(20)

        # Header Section
        # Main Title: "Login to Your Account"
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
        
        # Spacing handled by layout spacing (20px), maybe add a bit more after title?
        # The prompt says "Appropriate vertical spacing". 20px is decent.
        
        # Input Fields
        # Username
        self.username_input = InputField("Enter your username")
        # Password
        self.password_input = PasswordField("Enter your password")
        
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_input)

        # Error Message & Remember Me
        # Layout: "Remember me" below error (or same line if error hidden? Prompt says "Corrected Layout: 'Remember me' ... located below the error message")
        # Actually prompt says: "Corrected Layout: 'Remember me' checkbox is left-aligned with the input fields' content, located below the error message."
        
        # Error Message
        self.lbl_error = QLabel("Invalid credentials")
        self.lbl_error.setStyleSheet("""
            QLabel {
                font-family: Sans-serif;
                font-size: 13px;
                color: #DC3545;
            }
        """)
        self.lbl_error.hide() # Initially hidden
        form_layout.addWidget(self.lbl_error)

        # Remember Me Checkbox
        self.chk_remember = QCheckBox("Remember me")
        self.chk_remember.setCursor(Qt.PointingHandCursor)
        self.chk_remember.setStyleSheet("""
            QCheckBox {
                font-family: Sans-serif;
                font-size: 14px;
                color: #333333;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid #D1D5DB;
                border-radius: 4px;
                background: white;
            }
            QCheckBox::indicator:checked {
                background-color: #4C95ED;
                border-color: #4C95ED;
                image: url(resources/check.png); /* Assuming we might not have an image, but let's just use color for now or default style */
            }
        """) 
        # Note: Styling checkbox indicator fully often requires an image for the checkmark. 
        # For now I'll stick to simple styling or default indicator if no image available.
        # I will remove the indicator styling that requires image to avoid broken UI, 
        # or just style the box and let system draw check (which might not work well with custom background).
        # Let's keep it simple for the checkbox to ensure it renders.
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
        self.btn_login = PrimaryButton("Login", fixed_size=None)
        self.btn_login.setStyleSheet("""
            QPushButton {
                background-color: #4C95ED;
                color: white;
                font-family: Sans-serif;
                font-weight: bold;
                font-size: 16px;
                border-radius: 10px;
                padding: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #3B82F6; /* Slightly darker blue */
            }
            QPushButton:pressed {
                background-color: #2563EB;
            }
        """)
        # PrimaryButton might override style, but let's see. 
        # PrimaryButton usually sets style in init. I might need to use QPushButton if PrimaryButton is stubborn.
        # Let's check PrimaryButton implementation if I can. 
        # I'll assume standard QPushButton is safer for specific custom styling.
        
        from PySide6.QtWidgets import QPushButton
        self.btn_login = QPushButton("Login")
        self.btn_login.setCursor(Qt.PointingHandCursor)
        self.btn_login.setFixedHeight(44) # Similar height to inputs
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

        # Footer: "Don't have an account?" + "Create one" Link
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
    def __init__(self, viewModel: LoginViewModel):
        super().__init__()
        self.vm = viewModel

        self.setWindowTitle("Login")
        # Main Window Background: Dark Grey #3C4753
        self.setStyleSheet("QMainWindow { background-color: #3C4753; }")
        self.setMinimumSize(900, 700) # Adjusted to show the centered layout well

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
        self.card.setFixedWidth(450) # Medium width (400px to 500px)
        
        # Override Card Style for specific requirements
        # Shape: Rectangular with moderately rounded corners (12px to 18px) -> CardWidget has 18px
        # Color: Pure white -> CardWidget has white
        # Shadow: Prominent, soft, diffused (0px 8px 30px rgba(0, 0, 0, 0.2))
        shadow = QGraphicsDropShadowEffect(self.card)
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(8)
        shadow.setColor(QColor(0, 0, 0, 51)) # 0.2 alpha * 255 = 51
        self.card.setGraphicsEffect(shadow)

        # Form Layout
        form_layout = self.card.layout
        form_layout.setContentsMargins(40, 40, 40, 40) # Consistent padding
        form_layout.setSpacing(20)

        # Header Section
        # Main Title: "Login to Your Account"
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
        
        # Spacing handled by layout spacing (20px), maybe add a bit more after title?
        # The prompt says "Appropriate vertical spacing". 20px is decent.
        
        # Input Fields
        # Username
        self.username_input = InputField("Enter your username")
        # Password
        self.password_input = PasswordField("Enter your password")
        
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_input)

        # Error Message & Remember Me
        # Layout: "Remember me" below error (or same line if error hidden? Prompt says "Corrected Layout: 'Remember me' ... located below the error message")
        # Actually prompt says: "Corrected Layout: 'Remember me' checkbox is left-aligned with the input fields' content, located below the error message."
        
        # Error Message
        self.lbl_error = QLabel("Invalid credentials")
        self.lbl_error.setStyleSheet("""
            QLabel {
                font-family: Sans-serif;
                font-size: 13px;
                color: #DC3545;
            }
        """)
        self.lbl_error.hide() # Initially hidden
        form_layout.addWidget(self.lbl_error)

        # Remember Me Checkbox
        self.chk_remember = QCheckBox("Remember me")
        self.chk_remember.setCursor(Qt.PointingHandCursor)
        self.chk_remember.setStyleSheet("""
            QCheckBox {
                font-family: Sans-serif;
                font-size: 14px;
                color: #333333;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid #D1D5DB;
                border-radius: 4px;
                background: white;
            }
            QCheckBox::indicator:checked {
                background-color: #4C95ED;
                border-color: #4C95ED;
                image: url(resources/check.png); /* Assuming we might not have an image, but let's just use color for now or default style */
            }
        """) 
        # Note: Styling checkbox indicator fully often requires an image for the checkmark. 
        # For now I'll stick to simple styling or default indicator if no image available.
        # I will remove the indicator styling that requires image to avoid broken UI, 
        # or just style the box and let system draw check (which might not work well with custom background).
        # Let's keep it simple for the checkbox to ensure it renders.
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
        self.btn_login = PrimaryButton("Login", fixed_size=None)
        self.btn_login.setStyleSheet("""
            QPushButton {
                background-color: #4C95ED;
                color: white;
                font-family: Sans-serif;
                font-weight: bold;
                font-size: 16px;
                border-radius: 10px;
                padding: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #3B82F6; /* Slightly darker blue */
            }
            QPushButton:pressed {
                background-color: #2563EB;
            }
        """)
        # PrimaryButton might override style, but let's see. 
        # PrimaryButton usually sets style in init. I might need to use QPushButton if PrimaryButton is stubborn.
        # Let's check PrimaryButton implementation if I can. 
        # I'll assume standard QPushButton is safer for specific custom styling.
        
        from PySide6.QtWidgets import QPushButton
        self.btn_login = QPushButton("Login")
        self.btn_login.setCursor(Qt.PointingHandCursor)
        self.btn_login.setFixedHeight(44) # Similar height to inputs
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

        # Footer: "Don't have an account?" + "Create one" Link
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
        self.card.setGraphicsEffect(shadow)

        # Form Layout
        form_layout = self.card.layout
        form_layout.setContentsMargins(40, 40, 40, 40) # Consistent padding
        form_layout.setSpacing(20)

        # Header Section
        # Main Title: "Login to Your Account"
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
        
        # Spacing handled by layout spacing (20px), maybe add a bit more after title?
        # The prompt says "Appropriate vertical spacing". 20px is decent.
        
        # Input Fields
        # Username
        self.username_input = InputField("Enter your username")
        # Password
        self.password_input = PasswordField("Enter your password")
        
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_input)

        # Error Message & Remember Me
        # Layout: "Remember me" below error (or same line if error hidden? Prompt says "Corrected Layout: 'Remember me' ... located below the error message")
        # Actually prompt says: "Corrected Layout: 'Remember me' checkbox is left-aligned with the input fields' content, located below the error message."
        
        # Error Message
        self.lbl_error = QLabel("Invalid credentials")
        self.lbl_error.setStyleSheet("""
            QLabel {
                font-family: Sans-serif;
                font-size: 13px;
                color: #DC3545;
            }
        """)
        self.lbl_error.hide() # Initially hidden
        form_layout.addWidget(self.lbl_error)

        # Remember Me Checkbox
        self.chk_remember = QCheckBox("Remember me")
        self.chk_remember.setCursor(Qt.PointingHandCursor)
        self.chk_remember.setStyleSheet("""
            QCheckBox {
                font-family: Sans-serif;
                font-size: 14px;
                color: #333333;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid #D1D5DB;
                border-radius: 4px;
                background: white;
            }
            QCheckBox::indicator:checked {
                background-color: #4C95ED;
                border-color: #4C95ED;
                image: url(resources/check.png); /* Assuming we might not have an image, but let's just use color for now or default style */
            }
        """) 
        # Note: Styling checkbox indicator fully often requires an image for the checkmark. 
        # For now I'll stick to simple styling or default indicator if no image available.
        # I will remove the indicator styling that requires image to avoid broken UI, 
        # or just style the box and let system draw check (which might not work well with custom background).
        # Let's keep it simple for the checkbox to ensure it renders.
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
        self.btn_login = PrimaryButton("Login", fixed_size=None)
        self.btn_login.setStyleSheet("""
            QPushButton {
                background-color: #4C95ED;
                color: white;
                font-family: Sans-serif;
                font-weight: bold;
                font-size: 16px;
                border-radius: 10px;
                padding: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #3B82F6; /* Slightly darker blue */
            }
            QPushButton:pressed {
                background-color: #2563EB;
            }
        """)
        # PrimaryButton might override style, but let's see. 
        # PrimaryButton usually sets style in init. I might need to use QPushButton if PrimaryButton is stubborn.
        # Let's check PrimaryButton implementation if I can. 
        # I'll assume standard QPushButton is safer for specific custom styling.
        
        from PySide6.QtWidgets import QPushButton
        self.btn_login = QPushButton("Login")
        self.btn_login.setCursor(Qt.PointingHandCursor)
        self.btn_login.setFixedHeight(44) # Similar height to inputs
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

        # Footer: "Don't have an account?" + "Create one" Link
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

    # def _bind_viewmodel(self):
    #     self.username_input.textChanged.connect(self.vm.set_username)
    #     self.password_input.textChanged.connect(self.vm.set_password)

    #     # Bind Remember Me
    #     self.chk_remember.toggled.connect(self.vm.set_remember_me)
    #     self.chk_remember.setChecked(self.vm.rememberMe)
        
    #     # If credentials loaded, update inputs
    #     if self.vm.rememberMe:
    #         self.username_input.setText(self.vm.username)
    #         self.password_input.setText(self.vm.password)

    #     self.btn_login.clicked.connect(self.vm.loginCommand)
    #     self.btn_create_link.clicked.connect(self.vm.goToRegisterCommand)

    #     self.vm.loginRequest.connect(self._go_to_dashboard)
    #     self.vm.errorChanged.connect(self._on_error)
    #     self.vm.goToRegisterRequest.connect(self._go_to_create_account)

    # def _on_error(self, message):
    #     if message:
    #         self.lbl_error.setText(message)
    #         self.lbl_error.show()
    #     else:
    #         self.lbl_error.hide()

    # def _go_to_create_account(self):
    #     db_session = SessionLocal()
    #     create_vm = CreateAccountViewModel(db_session)
    #     self.create_account_window = CreateAccountView(create_vm)
    #     self.create_account_window.show()
    #     self.close()
        form_layout.setContentsMargins(40, 40, 40, 40) # Consistent padding
        form_layout.setSpacing(20)

        # Header Section
        # Main Title: "Login to Your Account"
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
        
        # Spacing handled by layout spacing (20px), maybe add a bit more after title?
        # The prompt says "Appropriate vertical spacing". 20px is decent.
        
        # Input Fields
        # Username
        self.username_input = InputField("Enter your username")
        # Password
        self.password_input = PasswordField("Enter your password")
        
        form_layout.addWidget(self.username_input)
        form_layout.addWidget(self.password_input)

        # Error Message & Remember Me
        # Layout: "Remember me" below error (or same line if error hidden? Prompt says "Corrected Layout: 'Remember me' ... located below the error message")
        # Actually prompt says: "Corrected Layout: 'Remember me' checkbox is left-aligned with the input fields' content, located below the error message."
        
        # Error Message
        self.lbl_error = QLabel("Invalid credentials")
        self.lbl_error.setStyleSheet("""
            QLabel {
                font-family: Sans-serif;
                font-size: 13px;
                color: #DC3545;
            }
        """)
        self.lbl_error.hide() # Initially hidden
        form_layout.addWidget(self.lbl_error)

        # Remember Me Checkbox
        self.chk_remember = QCheckBox("Remember me")
        self.chk_remember.setCursor(Qt.PointingHandCursor)
        self.chk_remember.setStyleSheet("""
            QCheckBox {
                font-family: Sans-serif;
                font-size: 14px;
                color: #333333;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid #D1D5DB;
                border-radius: 4px;
                background: white;
            }
            QCheckBox::indicator:checked {
                background-color: #4C95ED;
                border-color: #4C95ED;
                image: url(resources/check.png); /* Assuming we might not have an image, but let's just use color for now or default style */
            }
        """) 
        # Note: Styling checkbox indicator fully often requires an image for the checkmark. 
        # For now I'll stick to simple styling or default indicator if no image available.
        # I will remove the indicator styling that requires image to avoid broken UI, 
        # or just style the box and let system draw check (which might not work well with custom background).
        # Let's keep it simple for the checkbox to ensure it renders.
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
        self.btn_login = PrimaryButton("Login", fixed_size=None)
        self.btn_login.setStyleSheet("""
            QPushButton {
                background-color: #4C95ED;
                color: white;
                font-family: Sans-serif;
                font-weight: bold;
                font-size: 16px;
                border-radius: 10px;
                padding: 10px;
                border: none;
            }
            QPushButton:hover {
                background-color: #3B82F6; /* Slightly darker blue */
            }
            QPushButton:pressed {
                background-color: #2563EB;
            }
        """)
        # PrimaryButton might override style, but let's see. 
        # PrimaryButton usually sets style in init. I might need to use QPushButton if PrimaryButton is stubborn.
        # Let's check PrimaryButton implementation if I can. 
        # I'll assume standard QPushButton is safer for specific custom styling.
        
        from PySide6.QtWidgets import QPushButton
        self.btn_login = QPushButton("Login")
        self.btn_login.setCursor(Qt.PointingHandCursor)
        self.btn_login.setFixedHeight(44) # Similar height to inputs
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

        # Footer: "Don't have an account?" + "Create one" Link
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

    # def _bind_viewmodel(self):
    #     self.username_input.textChanged.connect(self.vm.set_username)
    #     self.password_input.textChanged.connect(self.vm.set_password)

    #     # Bind Remember Me
    #     self.chk_remember.toggled.connect(self.vm.set_remember_me)
    #     self.chk_remember.setChecked(self.vm.rememberMe)
        
    #     # If credentials loaded, update inputs
    #     if self.vm.rememberMe:
    #         self.username_input.setText(self.vm.username)
    #         self.password_input.setText(self.vm.password)

    #     self.btn_login.clicked.connect(self.vm.loginCommand)
    #     self.btn_create_link.clicked.connect(self.vm.goToRegisterCommand)

    #     self.vm.loginRequest.connect(self._go_to_dashboard)
    #     self.vm.errorChanged.connect(self._on_error)
    #     self.vm.goToRegisterRequest.connect(self._go_to_create_account)

    # def _on_error(self, message):
    #     if message:
    #         self.lbl_error.setText(message)
    #         self.lbl_error.show()
    #     else:
    #         self.lbl_error.hide()

    # def _go_to_create_account(self):
    #     db_session = SessionLocal()
    #     create_vm = CreateAccountViewModel(db_session)
    #     self.create_account_window = CreateAccountView(create_vm)
    #     self.create_account_window.show()
    #     self.close()

    def _go_to_dashboard(self):
        from views.dashboard.dashboard_view import DashboardView
        from viewmodels.dashboard.dashboard_viewmodel import DashboardViewModel
        
        dashboard_vm = DashboardViewModel(db_session=self.vm.db_session, current_user=self.vm.logged_user)
        self.dashboard_window = DashboardView(dashboard_vm)
        self.dashboard_window.show()
        self.close()