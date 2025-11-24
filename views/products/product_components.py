from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
    QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QComboBox, 
    QGraphicsDropShadowEffect, QFrame, QAbstractItemView
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QColor, QIcon, QFont

# --- Constants for Styling ---
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

class ProductSearchBar(QWidget):
    addProductClicked = Signal()
    searchChanged = Signal(str)

    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 20)
        layout.setSpacing(16)

        # Search Bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search products...")
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

        # Category Filter
        self.category_btn = QPushButton("Category Filter")
        self.category_btn.setStyleSheet(f"""
            QPushButton {{
                border: 1px solid {COLOR_BORDER};
                border-radius: 8px;
                padding: 10px 16px;
                font-family: {FONT_FAMILY};
                font-size: 14px;
                color: {COLOR_MEDIUM_GREY};
                background-color: {COLOR_WHITE};
                text-align: left;
            }}
        """)
        layout.addWidget(self.category_btn)

        # Status Filter
        self.status_btn = QPushButton("Status Filter")
        self.status_btn.setStyleSheet(f"""
            QPushButton {{
                border: 1px solid {COLOR_BORDER};
                border-radius: 8px;
                padding: 10px 16px;
                font-family: {FONT_FAMILY};
                font-size: 14px;
                color: {COLOR_MEDIUM_GREY};
                background-color: {COLOR_WHITE};
                text-align: left;
            }}
        """)
        layout.addWidget(self.status_btn)

        # Add New Product Button
        self.add_btn = QPushButton("Add New Product")
        self.add_btn.setCursor(Qt.PointingHandCursor)
        self.add_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_GREEN};
                color: {COLOR_WHITE};
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-family: {FONT_FAMILY};
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background-color: #218838;
            }}
        """)
        self.add_btn.clicked.connect(self.addProductClicked)
        layout.addWidget(self.add_btn)

class ProductTable(QWidget):
    editProductClicked = Signal(int) # product_id
    deleteProductClicked = Signal(int) # product_id

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Header
        header_lbl = QLabel("Search products")
        header_lbl.setStyleSheet(f"font-family: {FONT_FAMILY}; font-weight: bold; font-size: 16px; color: {COLOR_DARK_GREY};")
        layout.addWidget(header_lbl)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Product ID/Barcode", "Price", "Current", "Category", "Status", "Actions"])
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
                padding: 8px 12px;
                text-align: left;
            }}
            QTableWidget::item {{
                padding: 8px 12px;
                color: {COLOR_DARK_GREY};
                border-bottom: 1px solid #F5F5F5;
            }}
            QTableWidget::item:selected {{
                background-color: #F0F9FF;
                color: {COLOR_DARK_GREY};
            }}
        """)
        layout.addWidget(self.table)

    def set_products(self, products):
        self.table.setRowCount(len(products))
        for i, product in enumerate(products):
            # ID/Barcode
            self.table.setItem(i, 0, QTableWidgetItem(f"{product.barcode}"))
            
            # Price
            self.table.setItem(i, 1, QTableWidgetItem(f"${product.price}"))
            
            # Current (Stock with indicator)
            status_widget = QWidget()
            status_layout = QHBoxLayout(status_widget)
            status_layout.setContentsMargins(0, 0, 0, 0)
            status_layout.setAlignment(Qt.AlignLeft)
            
            indicator = QLabel()
            indicator.setFixedSize(10, 10)
            is_low_stock = product.quantity <= 10 # Default threshold
            color = COLOR_RED if is_low_stock else COLOR_GREEN
            indicator.setStyleSheet(f"background-color: {color}; border-radius: 5px;")
            
            text = QLabel(f"{product.quantity} in Stock")
            text.setStyleSheet(f"margin-left: 5px; color: {COLOR_DARK_GREY};")
            
            status_layout.addWidget(indicator)
            status_layout.addWidget(text)
            self.table.setCellWidget(i, 2, status_widget)
            
            # Category
            category_name = product.category.name if product.category else "Uncategorized"
            self.table.setItem(i, 3, QTableWidgetItem(category_name))
            
            # Status (Text)
            status_text = "Low Stock" if is_low_stock else "In Stock"
            self.table.setItem(i, 4, QTableWidgetItem(status_text))
            
            # Actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            actions_layout.setSpacing(10)
            actions_layout.setAlignment(Qt.AlignLeft)
            
            edit_btn = QPushButton("Edit")
            edit_btn.setCursor(Qt.PointingHandCursor)
            edit_btn.setStyleSheet(f"color: {COLOR_ORANGE}; background: transparent; border: none; font-weight: bold;")
            edit_btn.clicked.connect(lambda checked, pid=product.id: self.editProductClicked.emit(pid))
            
            delete_btn = QPushButton("Delete")
            delete_btn.setCursor(Qt.PointingHandCursor)
            delete_btn.setStyleSheet(f"color: {COLOR_RED}; background: transparent; border: none; font-weight: bold;")
            delete_btn.clicked.connect(lambda checked, pid=product.id: self.deleteProductClicked.emit(pid))
            
            actions_layout.addWidget(edit_btn)
            actions_layout.addWidget(delete_btn)
            self.table.setCellWidget(i, 5, actions_widget)

class PaginationControls(QWidget):
    prevClicked = Signal()
    nextClicked = Signal()

    def __init__(self):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 20, 0, 0)
        
        self.info_lbl = QLabel("Showing 0-0 of 0 products")
        self.info_lbl.setStyleSheet(f"color: {COLOR_DARK_GREY}; font-family: {FONT_FAMILY};")
        layout.addWidget(self.info_lbl)
        
        layout.addStretch()
        
        self.prev_btn = QPushButton("<< Prev")
        self.prev_btn.setCursor(Qt.PointingHandCursor)
        self.prev_btn.setStyleSheet(self._get_btn_style())
        self.prev_btn.clicked.connect(self.prevClicked)
        layout.addWidget(self.prev_btn)
        
        self.page_lbl = QPushButton("1")
        self.page_lbl.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_NAVY};
                color: {COLOR_WHITE};
                border-radius: 4px;
                padding: 5px 12px;
                font-family: {FONT_FAMILY};
                border: none;
            }}
        """)
        layout.addWidget(self.page_lbl)
        
        self.next_btn = QPushButton("Next >>")
        self.next_btn.setCursor(Qt.PointingHandCursor)
        self.next_btn.setStyleSheet(self._get_btn_style())
        self.next_btn.clicked.connect(self.nextClicked)
        layout.addWidget(self.next_btn)

    def _get_btn_style(self):
        return f"""
            QPushButton {{
                background-color: {COLOR_WHITE};
                color: {COLOR_DARK_GREY};
                border: 1px solid {COLOR_BORDER};
                border-radius: 4px;
                padding: 5px 10px;
                font-family: {FONT_FAMILY};
            }}
            QPushButton:hover {{
                background-color: #F5F5F5;
            }}
        """

    def update_state(self, current_page, total_pages, total_items, per_page):
        start = (current_page - 1) * per_page + 1 if total_items > 0 else 0
        end = min(current_page * per_page, total_items)
        self.info_lbl.setText(f"Showing {start}-{end} of {total_items} products")
        self.page_lbl.setText(str(current_page))
        
        self.prev_btn.setEnabled(current_page > 1)
        self.next_btn.setEnabled(current_page < total_pages)

class AddEditProductDialog(QDialog):
    def __init__(self, parent=None, product=None, categories=None):
        super().__init__(parent)
        self.product_id = product.id if product else None
        self.categories = categories or []
        self.setWindowTitle("Add/Edit Product")
        self.setFixedSize(450, 650)
        self.setStyleSheet(f"background-color: {COLOR_WHITE};")
        
        # Remove default frame and make it look like a card
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
        header = QLabel("Add/Edit Product")
        header.setStyleSheet(f"color: {COLOR_NAVY}; font-size: 20px; font-weight: bold; font-family: {FONT_FAMILY}; border: none;")
        card_layout.addWidget(header)
        
        # Fields
        self.name_input = self._create_input("Product Name", "📦 Product Name", product.name if product else "")
        card_layout.addWidget(self.name_input)
        
        self.barcode_input = self._create_input("Barcode", "🔢 Barcode", product.barcode if product else "", is_barcode=True)
        card_layout.addWidget(self.barcode_input)
        
        self.price_input = self._create_input("Price", "💲 Price", str(product.price) if product else "")
        card_layout.addWidget(self.price_input)
        
        self.quantity_input = self._create_input("Quantity", "📊 Quantity", str(product.quantity) if product else "")
        card_layout.addWidget(self.quantity_input)
        
        # Category Dropdown
        card_layout.addWidget(QLabel("📂 Category"))
        self.category_combo = QComboBox()
        self.category_combo.addItem("Select Category", None)
        for cat in self.categories:
            self.category_combo.addItem(cat.name, cat.id)
            
        if product and product.category_id:
            index = self.category_combo.findData(product.category_id)
            if index >= 0:
                self.category_combo.setCurrentIndex(index)
                
        self.category_combo.setStyleSheet(f"""
            QComboBox {{
                border: 1px solid {COLOR_BORDER};
                border-radius: 6px;
                padding: 10px;
                font-family: {FONT_FAMILY};
                color: {COLOR_DARK_GREY};
                background-color: {COLOR_WHITE};
            }}
            QComboBox::drop-down {{
                border: none;
            }}
        """)
        card_layout.addWidget(self.category_combo)
        
        card_layout.addStretch()
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_WHITE};
                color: {COLOR_DARK_GREY};
                border: 1px solid {COLOR_BORDER};
                border-radius: 6px;
                padding: 8px 20px;
                font-weight: bold;
                font-family: {FONT_FAMILY};
            }}
            QPushButton:hover {{
                background-color: #F5F5F5;
            }}
        """)
        cancel_btn.clicked.connect(self.reject)
        
        save_btn = QPushButton("Save")
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_GREEN};
                color: {COLOR_WHITE};
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-weight: bold;
                font-family: {FONT_FAMILY};
            }}
            QPushButton:hover {{
                background-color: #218838;
            }}
        """)
        save_btn.clicked.connect(self.accept)
        
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(save_btn)
        card_layout.addLayout(btn_layout)
        
        main_layout.addWidget(card)

    def _create_input(self, placeholder, label_text, text="", is_barcode=False):
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(5)
        
        label = QLabel(label_text)
        label.setStyleSheet(f"font-weight: bold; color: {COLOR_DARK_GREY};")
        layout.addWidget(label)
        
        input_container = QWidget()
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(10)
        
        inp = QLineEdit()
        inp.setPlaceholderText(placeholder)
        inp.setText(text)
        inp.setStyleSheet(f"""
            QLineEdit {{
                border: 1px solid {COLOR_BORDER};
                border-radius: 6px;
                padding: 10px;
                font-family: {FONT_FAMILY};
                color: {COLOR_DARK_GREY};
                background-color: {COLOR_WHITE};
            }}
        """)
        input_layout.addWidget(inp)
        
        if is_barcode:
            generate_btn = QPushButton("Generate")
            generate_btn.setCursor(Qt.PointingHandCursor)
            generate_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {COLOR_NAVY};
                    color: {COLOR_WHITE};
                    border: none;
                    border-radius: 6px;
                    padding: 10px 15px;
                    font-weight: bold;
                    font-family: {FONT_FAMILY};
                }}
                QPushButton:hover {{
                    background-color: #1E2A47;
                }}
            """)
            generate_btn.clicked.connect(lambda: self.generate_barcode(inp))
            input_layout.addWidget(generate_btn)
            
        layout.addWidget(input_container)
        return container

    def generate_barcode(self, input_field):
        # Generate a unique 12-digit barcode
        import random
        import string
        barcode = ''.join(random.choices(string.digits, k=12))
        input_field.setText(barcode)

    def get_data(self):
        return {
            "name": self.name_input.findChild(QLineEdit).text(),
            "barcode": self.barcode_input.findChild(QLineEdit).text(),
            "price": self.price_input.findChild(QLineEdit).text(),
            "quantity": self.quantity_input.findChild(QLineEdit).text(),
            "category_id": self.category_combo.currentData(),
            "low_stock_threshold": "10" # Default value as we removed the input
        }
