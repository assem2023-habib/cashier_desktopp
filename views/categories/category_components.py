from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
    QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QFrame, 
    QAbstractItemView
)
from PySide6.QtCore import Qt, Signal

# --- Constants for Styling ---
COLOR_WHITE = "#FFFFFF"
COLOR_DARK_GREY = "#333333"
COLOR_LIGHT_GREY = "#9CA3AF"
COLOR_BORDER = "#D1D5DB"
COLOR_GREEN = "#28A745"
COLOR_RED = "#DC3545"
COLOR_NAVY = "#2F3C64"
COLOR_ORANGE = "#ED6B6B"
FONT_FAMILY = "Sans-serif"

class CategoryTable(QWidget):
    editClicked = Signal(object) # Category object
    deleteClicked = Signal(int) # category_id

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Header
        header_lbl = QLabel("Categories")
        header_lbl.setStyleSheet(f"font-family: {FONT_FAMILY}; font-weight: bold; font-size: 16px; color: {COLOR_DARK_GREY};")
        layout.addWidget(header_lbl)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Actions"])
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
                font-size: 16px;
            }}
            QHeaderView::section {{
                background-color: {COLOR_WHITE};
                color: {COLOR_DARK_GREY};
                font-weight: bold;
                font-size: 16px;
                border: none;
                border-bottom: 2px solid #F0F0F0;
                padding: 16px;
                text-align: left;
            }}
            QTableWidget::item {{
                padding: 16px;
                color: {COLOR_DARK_GREY};
                border-bottom: 1px solid #F5F5F5;
            }}
            QTableWidget::item:selected {{
                background-color: #F0F9FF;
                color: {COLOR_DARK_GREY};
            }}
        """)
        layout.addWidget(self.table)
        
        self.categories = []

    def set_categories(self, categories):
        self.categories = categories
        self.table.setRowCount(len(categories))
        for i, category in enumerate(categories):
            # ID
            self.table.setItem(i, 0, QTableWidgetItem(str(category.id)))
            
            # Name
            self.table.setItem(i, 1, QTableWidgetItem(category.name))
            
            # Actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(5, 5, 5, 5)
            actions_layout.setSpacing(10)
            actions_layout.setAlignment(Qt.AlignLeft)
            
            edit_btn = QPushButton("Edit")
            edit_btn.setCursor(Qt.PointingHandCursor)
            edit_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: #E3F2FD;
                    color: {COLOR_NAVY};
                    border: 1px solid #BBDEFB;
                    border-radius: 6px;
                    padding: 6px 12px;
                    font-weight: bold;
                    font-size: 14px;
                }}
                QPushButton:hover {{
                    background-color: #BBDEFB;
                }}
            """)
            edit_btn.clicked.connect(lambda checked, c=category: self.editClicked.emit(c))
            
            delete_btn = QPushButton("Delete")
            delete_btn.setCursor(Qt.PointingHandCursor)
            delete_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: #FFEBEE;
                    color: {COLOR_RED};
                    border: 1px solid #FFCDD2;
                    border-radius: 6px;
                    padding: 6px 12px;
                    font-weight: bold;
                    font-size: 14px;
                }}
                QPushButton:hover {{
                    background-color: #FFCDD2;
                }}
            """)
            delete_btn.clicked.connect(lambda checked, cid=category.id: self.deleteClicked.emit(cid))
            
            actions_layout.addWidget(edit_btn)
            actions_layout.addWidget(delete_btn)
            self.table.setCellWidget(i, 2, actions_widget)

class AddEditCategoryDialog(QDialog):
    def __init__(self, parent=None, category=None):
        super().__init__(parent)
        self.category = category
        self.setWindowTitle("Edit Category" if category else "Add New Category")
        self.setFixedSize(400, 250)
        self.setStyleSheet(f"background-color: {COLOR_WHITE};")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Title
        title = QLabel("Edit Category" if category else "Add New Category")
        title.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {COLOR_DARK_GREY}; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Category Name")
        self.name_input.setStyleSheet(self._input_style())
        if category:
            self.name_input.setText(category.name)
        layout.addWidget(QLabel("Name"))
        layout.addWidget(self.name_input)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setCursor(Qt.PointingHandCursor)
        cancel_btn.setStyleSheet(f"background-color: {COLOR_LIGHT_GREY}; color: white; border-radius: 4px; padding: 8px 16px;")
        cancel_btn.clicked.connect(self.reject)
        
        save_btn = QPushButton("Save")
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.setStyleSheet(f"background-color: {COLOR_GREEN}; color: white; border-radius: 4px; padding: 8px 16px;")
        save_btn.clicked.connect(self.accept)
        
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(save_btn)
        layout.addLayout(btn_layout)

    def _input_style(self):
        return f"""
            border: 1px solid {COLOR_BORDER};
            border-radius: 4px;
            padding: 8px;
            font-family: {FONT_FAMILY};
            color: {COLOR_DARK_GREY};
        """

    def get_data(self):
        return {
            "name": self.name_input.text()
        }
