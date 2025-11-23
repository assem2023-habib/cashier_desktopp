from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QLabel, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QLinearGradient, QColor, QBrush

from viewmodels.auth.create_account_viewmodel import CreateAccountViewModel

# Components
from views.components.labels import TitleLabel, SubtitleLabel
from views.components.input_field import InputField
from views.components.password_field import PasswordField
from views.components.primary_button import PrimaryButton
from views.components.card_widget import CardWidget

class CreateAccountView(QMainWindow):
    def __init__(self, viewModel: CreateAccountViewModel):
        super().__init__()
        self.vm = viewModel
        self.setWindowTitle("Create Account")
        self.setMinimumSize(900, 700) # Increased size to show the layout better

        self._build_ui()
        self._bind_viewmodel()

    def _build_ui(self):
        # 1. Main Window Background (Gradient)
        self.setAutoFillBackground(True)
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#F5F5F5"))
        gradient.setColorAt(1.0, QColor("#E0E0E0"))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

        # Central Widget
        central = QWidget()
        self.setCentralWidget(central)
        
        # Main Layout (Centering the card)
        main_layout = QVBoxLayout(central)
        main_layout.setAlignment(Qt.AlignCenter)
        
        # 2. Card Container
        self.card = CardWidget()
        # Width: Approximately 60-70% of the screen width (assuming screen/window width)
        # We can set a fixed width or max width for the card to look good
        self.card.setFixedWidth(500) # Reasonable width for a form
        
        # Form Layout inside the card
        form_layout = self.card.layout # Access the layout we created in CardWidget
        form_layout.setSpacing(24) # Vertical spacing between elements

        # 3. Header Section
        header_layout = QVBoxLayout()
        header_layout.setSpacing(8)
        title = TitleLabel("Create Account")
        subtitle = SubtitleLabel("Sign up for a new account.")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        
        form_layout.addLayout(header_layout)

        # 4. Input Fields
        inputs_layout = QVBoxLayout()
        inputs_layout.setSpacing(16)
        
        self.username_input = InputField("Username", icon="👤")
        self.password_input = PasswordField("Password")
        self.confirm_input = PasswordField("Confirm Password")
        
        inputs_layout.addWidget(self.username_input)
        inputs_layout.addWidget(self.password_input)
        inputs_layout.addWidget(self.confirm_input)
        
        form_layout.addLayout(inputs_layout)

        # 5. Action Buttons Section
        actions_layout = QVBoxLayout()
        actions_layout.setSpacing(16)
        
        # "Create Account" Button
        self.btn_create = PrimaryButton("Create Account", fixed_size=None)
        # Make it full width of the form (which is handled by layout, but button has fixed size by default)
        self.btn_create.setFixedWidth(420) # Match input width approx (500 - 40*2 padding = 420)
        # Or better, let it expand? The prompt says "Same width as the input fields"
        # Input fields in InputField component are expanding but contained.
        # Let's just set it to match the available width in the card
        self.btn_create.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        actions_layout.addWidget(self.btn_create)
        
        # Footer: "Already have an account?" + "Login" Button
        footer_layout = QHBoxLayout()
        footer_layout.setAlignment(Qt.AlignCenter)
        footer_layout.setSpacing(4)
        
        lbl_already = QLabel("Already have an account?")
        lbl_already.setStyleSheet("font-size: 14px; color: #6B7280; font-family: Sans-serif;")
        
        self.btn_login = PrimaryButton(
            "Login",
            color="transparent",
            text_color="#6B7280",
            hover_color="#F5F5F5", # Light grey hover
            fixed_size=None
        )
        self.btn_login.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #6B7280;
                border: 1px solid #D1D5DB;
                border-radius: 6px;
                padding: 4px 12px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F5F5F5;
            }
        """)
        # The PrimaryButton class overrides setStyleSheet in _apply_style, so we might need to be careful.
        # Actually PrimaryButton logic might overwrite our custom stylesheet if we use setColor.
        # But here we just want a simple button. 
        # Let's use a standard QPushButton for Login if PrimaryButton is too opinionated, 
        # OR configure PrimaryButton to match.
        # PrimaryButton has `_apply_style`. 
        # Let's just use PrimaryButton and trust its logic if we pass the right colors, 
        # BUT it doesn't support border in `_apply_style`.
        # So I should probably just use a standard QPushButton for the Login button or modify PrimaryButton to support borders.
        # Given the prompt "Border: Thin, light grey border", PrimaryButton doesn't seem to support it via init.
        # I'll use a standard QPushButton for the login button to be safe and exact.
        
        from PySide6.QtWidgets import QPushButton
        self.btn_login = QPushButton("Login")
        self.btn_login.setCursor(Qt.PointingHandCursor)
        self.btn_login.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #6B7280;
                border: 1px solid #D1D5DB;
                border-radius: 6px;
                padding: 6px 16px;
                font-size: 16px;
                font-weight: bold;
                font-family: Sans-serif;
            }
            QPushButton:hover {
                background-color: #F5F5F5;
            }
        """)
        
        footer_layout.addWidget(lbl_already)
        footer_layout.addWidget(self.btn_login)
        
        actions_layout.addLayout(footer_layout)
        
        form_layout.addLayout(actions_layout)
        
        main_layout.addWidget(self.card)

    def resizeEvent(self, event):
        # Update gradient on resize
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#F5F5F5"))
        gradient.setColorAt(1.0, QColor("#E0E0E0"))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)
        super().resizeEvent(event)

    def _bind_viewmodel(self):
        self.username_input.textChanged(self.vm.set_username)
        self.password_input.textChanged(self.vm.set_password)
        self.confirm_input.textChanged(self.vm.set_confirmed_password)

        self.btn_create.clicked.connect(self.vm.createCommand)
        self.btn_login.clicked.connect(self._go_to_login) # Changed to local method or VM method if exists

        self.vm.createAccountRequested.connect(self._go_to_login)
        self.vm.errorChanged.connect(lambda msg: QMessageBox.warning(self, "Error", msg) if msg else None)
        self.vm.successChanged.connect(lambda msg: QMessageBox.information(self, "Success", msg) if msg else None)

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QMessageBox, QLabel, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QLinearGradient, QColor, QBrush

from viewmodels.auth.create_account_viewmodel import CreateAccountViewModel

# Components
from views.components.labels import TitleLabel, SubtitleLabel
from views.components.input_field import InputField
from views.components.password_field import PasswordField
from views.components.primary_button import PrimaryButton
from views.components.card_widget import CardWidget

class CreateAccountView(QMainWindow):
    def __init__(self, viewModel: CreateAccountViewModel):
        super().__init__()
        self.vm = viewModel
        self.setWindowTitle("Create Account")
        self.setMinimumSize(900, 700) # Increased size to show the layout better

        self._build_ui()
        self._bind_viewmodel()

    def _build_ui(self):
        # 1. Main Window Background (Gradient)
        self.setAutoFillBackground(True)
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#F5F5F5"))
        gradient.setColorAt(1.0, QColor("#E0E0E0"))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

        # Central Widget
        central = QWidget()
        self.setCentralWidget(central)
        
        # Main Layout (Centering the card)
        main_layout = QVBoxLayout(central)
        main_layout.setAlignment(Qt.AlignCenter)
        
        # 2. Card Container
        self.card = CardWidget()
        # Width: Approximately 60-70% of the screen width (assuming screen/window width)
        # We can set a fixed width or max width for the card to look good
        self.card.setFixedWidth(500) # Reasonable width for a form
        
        # Form Layout inside the card
        form_layout = self.card.layout # Access the layout we created in CardWidget
        form_layout.setSpacing(24) # Vertical spacing between elements

        # 3. Header Section
        header_layout = QVBoxLayout()
        header_layout.setSpacing(8)
        title = TitleLabel("Create Account")
        subtitle = SubtitleLabel("Sign up for a new account.")
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        
        form_layout.addLayout(header_layout)

        # 4. Input Fields
        inputs_layout = QVBoxLayout()
        inputs_layout.setSpacing(16)
        
        self.username_input = InputField("Username", icon="👤")
        self.password_input = PasswordField("Password")
        self.confirm_input = PasswordField("Confirm Password")
        
        inputs_layout.addWidget(self.username_input)
        inputs_layout.addWidget(self.password_input)
        inputs_layout.addWidget(self.confirm_input)
        
        form_layout.addLayout(inputs_layout)

        # 5. Action Buttons Section
        actions_layout = QVBoxLayout()
        actions_layout.setSpacing(16)
        
        # "Create Account" Button
        self.btn_create = PrimaryButton("Create Account", fixed_size=None)
        # Make it full width of the form (which is handled by layout, but button has fixed size by default)
        self.btn_create.setFixedWidth(420) # Match input width approx (500 - 40*2 padding = 420)
        # Or better, let it expand? The prompt says "Same width as the input fields"
        # Input fields in InputField component are expanding but contained.
        # Let's just set it to match the available width in the card
        self.btn_create.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        actions_layout.addWidget(self.btn_create)
        
        # Footer: "Already have an account?" + "Login" Button
        footer_layout = QHBoxLayout()
        footer_layout.setAlignment(Qt.AlignCenter)
        footer_layout.setSpacing(4)
        
        lbl_already = QLabel("Already have an account?")
        lbl_already.setStyleSheet("font-size: 14px; color: #6B7280; font-family: Sans-serif;")
        
        self.btn_login = PrimaryButton(
            "Login",
            color="transparent",
            text_color="#6B7280",
            hover_color="#F5F5F5", # Light grey hover
            fixed_size=None
        )
        self.btn_login.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #6B7280;
                border: 1px solid #D1D5DB;
                border-radius: 6px;
                padding: 4px 12px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #F5F5F5;
            }
        """)
        # The PrimaryButton class overrides setStyleSheet in _apply_style, so we might need to be careful.
        # Actually PrimaryButton logic might overwrite our custom stylesheet if we use setColor.
        # But here we just want a simple button. 
        # Let's use a standard QPushButton for Login if PrimaryButton is too opinionated, 
        # OR configure PrimaryButton to match.
        # PrimaryButton has `_apply_style`. 
        # Let's just use PrimaryButton and trust its logic if we pass the right colors, 
        # BUT it doesn't support border in `_apply_style`.
        # So I should probably just use a standard QPushButton for the Login button or modify PrimaryButton to support borders.
        # Given the prompt "Border: Thin, light grey border", PrimaryButton doesn't seem to support it via init.
        # I'll use a standard QPushButton for the login button to be safe and exact.
        
        from PySide6.QtWidgets import QPushButton
        self.btn_login = QPushButton("Login")
        self.btn_login.setCursor(Qt.PointingHandCursor)
        self.btn_login.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #6B7280;
                border: 1px solid #D1D5DB;
                border-radius: 6px;
                padding: 6px 16px;
                font-size: 16px;
                font-weight: bold;
                font-family: Sans-serif;
            }
            QPushButton:hover {
                background-color: #F5F5F5;
            }
        """)
        
        footer_layout.addWidget(lbl_already)
        footer_layout.addWidget(self.btn_login)
        
        actions_layout.addLayout(footer_layout)
        
        form_layout.addLayout(actions_layout)
        
        main_layout.addWidget(self.card)

    def resizeEvent(self, event):
        # Update gradient on resize
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#F5F5F5"))
        gradient.setColorAt(1.0, QColor("#E0E0E0"))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)
        super().resizeEvent(event)

    def _bind_viewmodel(self):
        self.username_input.textChanged(self.vm.set_username)
        self.password_input.textChanged(self.vm.set_password)
        self.confirm_input.textChanged(self.vm.set_confirmed_password)

        self.btn_create.clicked.connect(self.vm.createCommand)
        self.btn_login.clicked.connect(self._go_to_login) # Changed to local method or VM method if exists

        self.vm.createAccountRequested.connect(self._go_to_login)
        self.vm.errorChanged.connect(lambda msg: QMessageBox.warning(self, "Error", msg) if msg else None)
        self.vm.successChanged.connect(lambda msg: QMessageBox.information(self, "Success", msg) if msg else None)

        self.vm.togglePasswordVisibilityRequested.connect(
            lambda state: self.confirm_input.input.setEchoMode(
                self.confirm_input.input.Normal if state else self.confirm_input.input.Password
            )
        )
    
    def _go_to_login(self):
        from views.auth.login_view import LoginView
        from viewmodels.auth.login_viewmodel import LoginViewModel
        from data.database import SessionLocal
        
        db_session = SessionLocal()
        login_vm = LoginViewModel(db_session)
        self.login_window = LoginView(login_vm)
        self.login_window.show()
        self.close()