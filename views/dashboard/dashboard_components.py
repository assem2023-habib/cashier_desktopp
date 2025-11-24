from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, 
                               QFrame, QSizePolicy, QListWidget, QListWidgetItem, QGridLayout, QTableWidget, QTableWidgetItem, QHeaderView)
from PySide6.QtCore import Qt, QSize, QTimer, QDateTime
from PySide6.QtGui import QColor, QIcon, QPainter, QBrush, QPen

# --- Top Bar ---
class TopBar(QFrame):
    def __init__(self, username=None, user_role=None):
        super().__init__()
        self.setFixedHeight(70)
        self.setStyleSheet("background-color: #FFFFFF; border-bottom: 1px solid #E0E0E0;")
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        
        # System Title
        title_layout = QHBoxLayout()
        icon_label = QLabel("🛒") # Placeholder for icon
        icon_label.setStyleSheet("font-size: 20px; color: #2F3C64;")
        title = QLabel("POSFlow")
        title.setStyleSheet("font-family: Sans-serif; font-weight: bold; font-size: 20px; color: #2F3C64;")
        title_layout.addWidget(icon_label)
        title_layout.addWidget(title)
        title_layout.setSpacing(10)
        
        layout.addLayout(title_layout)
        layout.addStretch()
        
        # User Info & Date/Time
        info_layout = QHBoxLayout()
        info_layout.setSpacing(20)
        
        # User label with dynamic data
        user_display = f"{username or 'Guest'} ({user_role or 'N/A'})"
        self.user_label = QLabel(f"User: {user_display}")
        # self.date_label = QLabel("Date: --") # Removed as per request
        self.time_label = QLabel("Time: --")
        
        for lbl in [self.user_label, self.time_label]:
            lbl.setStyleSheet("font-family: Sans-serif; font-size: 14px; color: #333333;")
            info_layout.addWidget(lbl)
            
        layout.addLayout(info_layout)
        layout.addSpacing(20)
        
        # Actions
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(10)
        
        self.btn_logout = QPushButton("Logout")
        self.btn_logout.setCursor(Qt.PointingHandCursor)
        self.btn_logout.setStyleSheet("""
            QPushButton {
                background-color: #B0D0F5;
                color: #2F3C64;
                border-radius: 8px;
                padding: 8px 16px;
                font-family: Sans-serif;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #90B0D5;
            }
        """)
        
        self.btn_settings = QPushButton("⚙️")
        self.btn_lock = QPushButton("🔒")
        
        for btn in [self.btn_settings, self.btn_lock]:
            btn.setCursor(Qt.PointingHandCursor)
            btn.setFixedSize(36, 36)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #333333;
                    font-size: 18px;
                    border: none;
                }
                QPushButton:hover {
                    color: #000000;
                }
            """)
            
        actions_layout.addWidget(self.btn_logout)
        actions_layout.addWidget(self.btn_settings)
        actions_layout.addWidget(self.btn_lock)
        
        layout.addLayout(actions_layout)
        
        # Start timer to update date/time every second
        self._update_datetime()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_datetime)
        self.timer.start(1000)  # Update every 1 second
    
    def _update_datetime(self):
        """Update time label with current values"""
        current_dt = QDateTime.currentDateTime()
        # self.date_label.setText(f"Date: {current_dt.toString('yyyy-MM-dd')}")
        self.time_label.setText(f"Time: {current_dt.toString('hh:mm:ss AP')}")

# --- Sidebar ---
class Sidebar(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(250)
        self.setStyleSheet("background-color: #2F3C64; border: none;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 20, 0, 20)
        layout.setSpacing(5)
        
        self.nav_list = QListWidget()
        self.nav_list.setFrameShape(QFrame.NoFrame)
        self.nav_list.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                outline: none;
            }
            QListWidget::item {
                color: #FFFFFF;
                padding: 15px 20px;
                font-family: Sans-serif;
                font-size: 16px;
                border-left: 4px solid transparent;
            }
            QListWidget::item:hover {
                background-color: #3E4C7A;
            }
            QListWidget::item:selected {
                background-color: #4A577B;
                border-left: 4px solid #FFFFFF;
                color: #FFFFFF;
            }
        """)
        
        items = [
            ("POS Screen", "🖥️"),
            ("Products", "📦"),
            ("Categories", "📂"),
            ("Reports", "📊"),
            ("Users", "👥"),
            ("Activity Log", "📝"),
            ("Settings", "⚙️")
        ]
        
        for text, icon in items:
            item = QListWidgetItem(f"{icon}   {text}")
            if text in ["Reports", "Users", "Activity Log"]:
                item.setText(f"{icon}   {text}   🔒")
            self.nav_list.addItem(item)
            
        self.nav_list.setCurrentRow(0) # Default active
        layout.addWidget(self.nav_list)

# --- Stat Card ---
class StatCard(QFrame):
    def __init__(self, title, value, value_color):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 12px;
                border: 1px solid #E0E0E0;
            }
        """)
        # Shadow effect can be added if needed, but simple border is clean too
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        lbl_title = QLabel(title)
        lbl_title.setStyleSheet("font-family: Sans-serif; font-size: 14px; color: #333333; border: none;")
        
        lbl_value = QLabel(value)
        lbl_value.setStyleSheet(f"font-family: Sans-serif; font-size: 24px; font-weight: bold; color: {value_color}; border: none;")
        
        layout.addWidget(lbl_title)
        layout.addWidget(lbl_value)

# --- Chart Card ---
# Using a placeholder for chart to avoid complex dependency if QtCharts not available or setup complexity
# But we can draw a simple line using QPainter
class ChartCard(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 12px;
                border: 1px solid #E0E0E0;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        header = QLabel("Sales for Last 7 Days")
        header.setStyleSheet("font-family: Sans-serif; font-size: 18px; font-weight: bold; color: #333333; border: none;")
        layout.addWidget(header)
        
        self.chart_area = ChartArea()
        layout.addWidget(self.chart_area)

class ChartArea(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("border: none;")
        self.setMinimumHeight(200)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Draw axes
        w = self.width()
        h = self.height()
        padding = 30
        
        painter.setPen(QPen(QColor("#D1D5DB"), 1))
        painter.drawLine(padding, h - padding, w - padding, h - padding) # X-axis
        painter.drawLine(padding, padding, padding, h - padding) # Y-axis
        
        # Draw line graph (Mock data)
        points = [20, 50, 30, 80, 60, 90, 70] # 0-100 scale
        
        step_x = (w - 2 * padding) / (len(points) - 1)
        scale_y = (h - 2 * padding) / 100
        
        path_points = []
        for i, val in enumerate(points):
            x = padding + i * step_x
            y = h - padding - val * scale_y
            path_points.append((x, y))
            
        painter.setPen(QPen(QColor("#28A745"), 3))
        for i in range(len(path_points) - 1):
            painter.drawLine(path_points[i][0], path_points[i][1], path_points[i+1][0], path_points[i+1][1])
            
        # Draw dots
        painter.setBrush(QBrush(QColor("#28A745")))
        for x, y in path_points:
            painter.drawEllipse(x - 4, y - 4, 8, 8)

# --- Activity Card ---
class ActivityCard(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 12px;
                border: 1px solid #E0E0E0;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        header = QLabel("Recent Activity")
        header.setStyleSheet("font-family: Sans-serif; font-size: 18px; font-weight: bold; color: #333333; border: none;")
        layout.addWidget(header)
        
        activities = [
            "Sale #125 - $20.50 (Completed)",
            "User login - Jane Doe",
            "Product update - SKU: 123",
            "Sale #124 - $15.75 (Completed)",
            "Receipt print - #123"
        ]
        
        for act in activities:
            lbl = QLabel(f"• {act}")
            lbl.setStyleSheet("font-family: Sans-serif; font-size: 14px; color: #333333; border: none; margin-bottom: 5px;")
            layout.addWidget(lbl)
            
        layout.addStretch()

# --- Low Stock Card ---
class LowStockCard(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background-color: #FFFFFF;
                border-radius: 12px;
                border: 1px solid #E0E0E0;
            }
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        header = QLabel("Low Stock Products")
        header.setStyleSheet("font-family: Sans-serif; font-size: 18px; font-weight: bold; color: #333333; border: none;")
        layout.addWidget(header)
        
        table = QTableWidget(5, 3)
        table.setHorizontalHeaderLabels(["Product Name", "Qty", "Status"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setVisible(False)
        table.setShowGrid(False)
        table.setStyleSheet("""
            QTableWidget {
                border: none;
                font-family: Sans-serif;
            }
            QHeaderView::section {
                background-color: white;
                border: none;
                border-bottom: 1px solid #E0E0E0;
                font-weight: bold;
                color: #333333;
                padding: 5px;
            }
            QTableWidget::item {
                padding: 5px;
                border-bottom: 1px solid #F0F0F0;
            }
        """)
        
        data = [
            ("Product A", "5", "Warning"),
            ("Product B", "2", "Critical"),
            ("Product C", "8", "Warning"),
            ("Product D", "0", "Critical"),
            ("Product E", "4", "Warning")
        ]
        
        for r, (name, qty, status) in enumerate(data):
            table.setItem(r, 0, QTableWidgetItem(name))
            table.setItem(r, 1, QTableWidgetItem(qty))
            
            item_status = QTableWidgetItem(status)
            if status == "Critical":
                item_status.setForeground(QColor("#DC3545"))
            else:
                item_status.setForeground(QColor("#FFC107"))
            table.setItem(r, 2, item_status)
            
        layout.addWidget(table)
        
        footer = QLabel("Action required: Order more stock!")
        footer.setStyleSheet("font-family: Sans-serif; font-size: 14px; color: #DC3545; text-decoration: underline; border: none; margin-top: 10px;")
        layout.addWidget(footer)
