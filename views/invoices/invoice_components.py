from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
    QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QFrame, 
    QAbstractItemView, QGraphicsDropShadowEffect
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor, QFont

# --- Constants for Styling (Reusing consistent styles) ---
COLOR_WHITE = "#FFFFFF"
COLOR_DARK_GREY = "#333333"
COLOR_LIGHT_GREY = "#9CA3AF"
COLOR_MEDIUM_GREY = "#6B7280"
COLOR_BORDER = "#D1D5DB"
COLOR_GREEN = "#28A745"
COLOR_RED = "#DC3545"
COLOR_ORANGE = "#ED6B6B"
COLOR_NAVY = "#2F3C64"
FONT_FAMILY = "Sans-serif"

class InvoiceSearchBar(QWidget):
    searchChanged = Signal(str)

    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 20)
        layout.setSpacing(16)

        # Search Bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by Invoice ID...")
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                border: 1px solid {COLOR_BORDER};
                border-radius: 8px;
                padding: 10px 16px;
                font-family: {FONT_FAMILY};
                font-size: 14px;
                color: {COLOR_DARK_GREY};
                background-color: {COLOR_WHITE};
            }}
        """)
        self.search_input.textChanged.connect(self.searchChanged)
        layout.addWidget(self.search_input, stretch=2)
        
        # Add stretch to keep search bar to the left or fill as needed
        layout.addStretch(1)

class InvoiceTable(QWidget):
    viewDetailsClicked = Signal(int) # invoice_id

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Header
        header_lbl = QLabel("Invoices")
        header_lbl.setStyleSheet(f"font-family: {FONT_FAMILY}; font-weight: bold; font-size: 16px; color: {COLOR_DARK_GREY};")
        layout.addWidget(header_lbl)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Invoice ID", "Date", "Customer", "Total Amount", "Status", "Actions"])
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)
        
        # Table Style
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {COLOR_WHITE};
                border: none;
                gridline-color: transparent;
                font-family: {FONT_FAMILY};
            }}
            QHeaderView::section {{
                background-color: {COLOR_WHITE};
                color: {COLOR_DARK_GREY};
                font-weight: bold;
                border: none;
                border-bottom: 2px solid #F0F0F0;
                padding: 12px;
                text-align: left;
            }}
            QTableWidget::item {{
                padding: 12px;
                color: {COLOR_DARK_GREY};
                border-bottom: 1px solid #F5F5F5;
            }}
            QTableWidget::item:selected {{
                background-color: #F0F9FF;
                color: {COLOR_DARK_GREY};
            }}
        """)
        layout.addWidget(self.table)

    def set_invoices(self, invoices):
        self.table.setRowCount(len(invoices))
        for i, invoice in enumerate(invoices):
            # ID
            self.table.setItem(i, 0, QTableWidgetItem(str(invoice.id)))
            
            # Date
            self.table.setItem(i, 1, QTableWidgetItem(invoice.date.strftime("%Y-%m-%d %H:%M")))
            
            # Customer (Handle None)
            customer_name = invoice.customer.name if invoice.customer else "Walk-in Customer"
            self.table.setItem(i, 2, QTableWidgetItem(customer_name))
            
            # Total Amount
            self.table.setItem(i, 3, QTableWidgetItem(f"${invoice.total_amount:.2f}"))
            
            # Status
            status_item = QTableWidgetItem(str(invoice.status.value))
            # Optional: Color code status
            self.table.setItem(i, 4, status_item)
            
            # Actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            actions_layout.setAlignment(Qt.AlignLeft)
            
            view_btn = QPushButton("View Details")
            view_btn.setCursor(Qt.PointingHandCursor)
            view_btn.setStyleSheet(f"color: {COLOR_NAVY}; background: transparent; border: none; font-weight: bold;")
            view_btn.clicked.connect(lambda checked, iid=invoice.id: self.viewDetailsClicked.emit(iid))
            
            actions_layout.addWidget(view_btn)
            self.table.setCellWidget(i, 5, actions_widget)

class InvoiceDetailDialog(QDialog):
    def __init__(self, parent=None, invoice_details=None):
        super().__init__(parent)
        self.setWindowTitle(f"Invoice #{invoice_details['invoice'].id} Details")
        self.setFixedSize(600, 500)
        self.setStyleSheet(f"background-color: {COLOR_WHITE};")
        
        # Remove default frame
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Card Container
        card = QFrame()
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_WHITE};
                border-radius: 12px;
                border: 1px solid {COLOR_BORDER};
            }}
        """)
        # Shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setYOffset(10)
        card.setGraphicsEffect(shadow)
        
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        title = QLabel(f"Invoice #{invoice_details['invoice'].id}")
        title.setStyleSheet(f"color: {COLOR_NAVY}; font-size: 20px; font-weight: bold; font-family: {FONT_FAMILY}; border: none;")
        
        close_btn = QPushButton("✕")
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet("background: transparent; border: none; font-size: 18px; color: #999;")
        close_btn.clicked.connect(self.accept)
        
        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(close_btn)
        card_layout.addLayout(header_layout)
        
        # Info
        info_layout = QHBoxLayout()
        date_lbl = QLabel(f"Date: {invoice_details['invoice'].date.strftime('%Y-%m-%d %H:%M')}")
        customer_name = invoice_details['invoice'].customer.name if invoice_details['invoice'].customer else "Walk-in Customer"
        cust_lbl = QLabel(f"Customer: {customer_name}")
        
        for lbl in [date_lbl, cust_lbl]:
            lbl.setStyleSheet(f"color: {COLOR_DARK_GREY}; font-family: {FONT_FAMILY}; font-size: 14px; border: none;")
            info_layout.addWidget(lbl)
            
        card_layout.addLayout(info_layout)
        
        # Items Table
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Product", "Qty", "Unit Price", "Total"])
        table.verticalHeader().setVisible(False)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setShowGrid(False)
        table.setStyleSheet(f"""
            QTableWidget {{ border: 1px solid {COLOR_BORDER}; border-radius: 4px; }}
            QHeaderView::section {{ background-color: #F8F9FA; border: none; padding: 8px; font-weight: bold; }}
            QTableWidget::item {{ padding: 8px; border-bottom: 1px solid #EEE; }}
        """)
        
        items = invoice_details['items']
        table.setRowCount(len(items))
        for i, item in enumerate(items):
            table.setItem(i, 0, QTableWidgetItem(item.product.name if item.product else "Unknown"))
            table.setItem(i, 1, QTableWidgetItem(str(item.quantity)))
            table.setItem(i, 2, QTableWidgetItem(f"${item.unit_price:.2f}"))
            table.setItem(i, 3, QTableWidgetItem(f"${item.total_price:.2f}"))
            
        card_layout.addWidget(table)
        
        # Total
        total_lbl = QLabel(f"Total Amount: ${invoice_details['invoice'].total_amount:.2f}")
        total_lbl.setStyleSheet(f"color: {COLOR_GREEN}; font-size: 18px; font-weight: bold; font-family: {FONT_FAMILY}; border: none; margin-top: 10px;")
        total_lbl.setAlignment(Qt.AlignRight)
        card_layout.addWidget(total_lbl)
        
        main_layout.addWidget(card)
