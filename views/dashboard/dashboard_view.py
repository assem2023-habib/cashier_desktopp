from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget
from PySide6.QtCore import Qt

from viewmodels.dashboard.dashboard_viewmodel import DashboardViewModel
from views.dashboard.dashboard_components import TopBar, Sidebar
from views.products.product_management_view import ProductManagementView
from views.dashboard.summary_view import SummaryView
from views.invoices.invoice_management_view import InvoiceManagementView

class DashboardView(QMainWindow):
    def __init__(self, viewModel: DashboardViewModel):
        super().__init__()
        self.vm = viewModel
        self.setWindowTitle("POSFlow Dashboard")
        self.setMinimumSize(1280, 800)
        
        # Main Layout
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 1. Top Bar
        self.top_bar = TopBar()
        main_layout.addWidget(self.top_bar)
        
        # 2. Content Area (Sidebar + Main Content)
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = Sidebar()
        content_layout.addWidget(self.sidebar)
        
        # Main Content - Stacked Widget
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("background-color: #FFFFFF;")
        
        # View 0: Summary (POS Screen / Dashboard)
        self.summary_view = SummaryView(self.vm)
        self.stacked_widget.addWidget(self.summary_view)
        
        # View 1: Products
        self.product_view = ProductManagementView()
        self.stacked_widget.addWidget(self.product_view)
        
        # View 2: Reports (Placeholder)
        self.reports_view = QWidget() # Placeholder
        self.stacked_widget.addWidget(self.reports_view)

        # View 3: Users (Placeholder)
        self.users_view = QWidget() # Placeholder
        self.stacked_widget.addWidget(self.users_view)

        # View 4: Activity Log (Invoices)
        # Re-purposing "Activity Log" or adding "Invoices" to sidebar?
        # User asked for "Invoice" UI. Let's assume it maps to "Activity Log" or we should add "Invoices" to sidebar.
        # Sidebar items: POS Screen, Products, Reports, Users, Activity Log, Settings.
        # Let's map "Activity Log" to Invoices for now as it fits best, or add new item.
        # Given the prompt "Invoice, Invoice Item", let's map it to a new view.
        # But wait, sidebar is fixed in components. Let's check sidebar items again.
        # Items: POS Screen, Products, Reports, Users, Activity Log, Settings.
        # I will map "Activity Log" (Index 4) to InvoiceManagementView for this task.
        
        self.invoice_view = InvoiceManagementView()
        self.stacked_widget.addWidget(self.invoice_view) 
        
        # View 5: Settings (Placeholder)
        self.settings_view = QWidget()
        self.stacked_widget.addWidget(self.settings_view)

        content_layout.addWidget(self.stacked_widget)
        
        main_layout.addLayout(content_layout)
        
        self._bind_viewmodel()

    def _bind_viewmodel(self):
        # Bind Logout Button
        self.top_bar.btn_logout.clicked.connect(self.vm.logout)
        
        # Handle Logout Signal
        self.vm.logoutRequested.connect(self._handle_logout)
        
        # Bind Sidebar Navigation
        self.sidebar.nav_list.currentRowChanged.connect(self._on_nav_changed)

    def _on_nav_changed(self, index):
        # Map sidebar index to stacked widget index
        # 0: POS Screen -> SummaryView
        # 1: Products -> ProductManagementView
        # 2: Reports -> Placeholder
        # 3: Users -> Placeholder
        # 4: Activity Log -> InvoiceManagementView
        # 5: Settings -> Placeholder
        
        if index < self.stacked_widget.count():
            self.stacked_widget.setCurrentIndex(index)

    def _handle_logout(self):
        from views.auth.login_view import LoginView
        from viewmodels.auth.login_viewmodel import LoginViewModel
        from data.database import SessionLocal
        
        db_session = SessionLocal()
        login_vm = LoginViewModel(db_session)
        self.login_window = LoginView(login_vm)
        self.login_window.show()
        self.close()
