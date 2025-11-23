from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea, QLabel
from PySide6.QtCore import Qt

from views.dashboard.dashboard_components import StatCard, ChartCard, ActivityCard, LowStockCard
from viewmodels.dashboard.dashboard_viewmodel import DashboardViewModel

class SummaryView(QWidget):
    def __init__(self, viewModel: DashboardViewModel):
        super().__init__()
        self.vm = viewModel
        
        self._build_ui()

    def _build_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background-color: #F5F7FA; border: none;")
        
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background-color: #F5F7FA;")
        self.scroll_layout = QVBoxLayout(scroll_content)
        self.scroll_layout.setContentsMargins(30, 30, 30, 30)
        self.scroll_layout.setSpacing(30)
        
        # --- Quick Stats ---
        lbl_stats = QLabel("Quick Stats")
        lbl_stats.setStyleSheet("font-family: Sans-serif; font-size: 20px; font-weight: bold; color: #333333;")
        self.scroll_layout.addWidget(lbl_stats)
        
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)
        
        # Using data from ViewModel (which currently has mock data)
        self.card_sales = StatCard("Total Daily Sales", self.vm.dailySales, "#28A745")
        self.card_receipts = StatCard("Number of Receipts Today", self.vm.receiptsCount, "#333333")
        self.card_avg = StatCard("Average Receipt Value", self.vm.avgReceiptValue, "#4C95ED")
        self.card_stock = StatCard("Low Stock Products", self.vm.lowStockCount, "#FFC107")
        
        stats_layout.addWidget(self.card_sales)
        stats_layout.addWidget(self.card_receipts)
        stats_layout.addWidget(self.card_avg)
        stats_layout.addWidget(self.card_stock)
        
        self.scroll_layout.addLayout(stats_layout)
        
        # --- Charts & Activity ---
        mid_section_layout = QHBoxLayout()
        mid_section_layout.setSpacing(30)
        
        self.chart_card = ChartCard()
        self.activity_card = ActivityCard()
        
        mid_section_layout.addWidget(self.chart_card, 2)
        mid_section_layout.addWidget(self.activity_card, 1)
        
        self.scroll_layout.addLayout(mid_section_layout)
        
        # --- Low Stock Table ---
        self.low_stock_card = LowStockCard()
        self.scroll_layout.addWidget(self.low_stock_card)
        
        self.scroll_layout.addStretch()
        
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
