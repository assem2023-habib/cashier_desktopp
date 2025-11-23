from PySide6.QtWidgets import (
    QApplication, QWidget, QMainWindow, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout,
    QSpacerItem, QSizePolicy, QToolButton, QWidgetAction
)
from PySide6.QtGui import QIcon, QFont, QActionEvent, QColor, QAction
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QGraphicsDropShadowEffect
import sys

COLOR_BG_TOP= "#F5F5F5"
COLOR_BG_BOTTOM = "#E0E0E0"
COLOR_FRAME_BG = "#FFFFFF"
COLOR_PRIMARY = "#2F3C64"
COLOR_MUTED = "#6B7280"
COLOR_PLACEHOLDER = "#9CA3AF"
COLOR_INPUT_BORDER = "#D1D5DB"

FONT_FAMILY = "Sans-serif"
TITLE_FONT_SIZE = 26
SUBTITLE_FONT_SIZE = 13
INPUT_FONT_SIZE = 12
BUTTON_FONT_SIZE = 16

class CreateAccountWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create Account")
        self.setMinimumSize(900, 700)
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QMainWindow {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                             stop:0 {COLOR_BG_TOP}, stop:1 {COLOR_BG_BOTTOM});
            }}
        """)
        central= QWidget()
        self.setCentralWidget(central)

        outer_layout= QVBoxLayout(central)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)

        outer_layout.addStretch(1)

        container= QWidget()
        container.setObjectName("card")
        container.setFixedWidth(int(self.width() * 0.65))
        container.setFixedHeight(int(self.height() * 0.75))

        self.container= container

        shadow= QGraphicsDropShadowEffect(blurRadius= 24, xOffset= 0, yOffset= 8)
        shadow.setColor(QColor(0, 0, 0, 25))
        container.setGraphicsEffect(shadow)

        container.setStyleSheet(f"""
            QWidget#card {{
                background: {COLOR_FRAME_BG};
                border-radius: 12px;
            }}
        """)

        card_layout = QVBoxLayout(container)
        card_layout.setContentsMargins(40, 30, 40, 30)
        card_layout.setSpacing(18)

        title = QLabel("Create Account")
        title_font = QFont(FONT_FAMILY, TITLE_FONT_SIZE)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet(f"color: {COLOR_PRIMARY};")

        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        card_layout.addWidget(title)

        subtitle = QLabel("Welcom")
        subtitle_font = QFont(FONT_FAMILY, SUBTITLE_FONT_SIZE)
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet(f"color: {COLOR_MUTED};")
        subtitle.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        card_layout.addWidget(subtitle)

        card_layout.addSpacing(6)

        form_widget = QWidget()
        form_layout = QVBoxLayout(form_widget)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(12)

        def make_input(placeholder_text, left_icon_unicode=None, echo_mode=QLineEdit.Normal):
            line = QLineEdit()
            line.setPlaceholderText(placeholder_text)
            line.setEchoMode(echo_mode)
            line.setFixedHeight(44)
            line.setStyleSheet(f"""
                QLineEdit {{
                    background: {COLOR_FRAME_BG};
                    border: 1px solid {COLOR_INPUT_BORDER};
                    border-radius: 8px;
                    padding-left: 36px;
                    padding-right: 12px;
                    color: #000000;
                    font-size: {INPUT_FONT_SIZE}px;
                }}
                QLineEdit:focus {{
                    border: 1px solid {COLOR_INPUT_BORDER};
                    background: {COLOR_FRAME_BG};
                }}
            """)

            line.setPlaceholderText(placeholder_text)

            line.setStyleSheet(line.styleSheet() + f" QLineEdit {{ color: #000; }} QLineEdit::placeholder {{ color: {COLOR_PLACEHOLDER}; }}")

            if left_icon_unicode:
                act = QAction(left_icon_unicode, line)
                line.addAction(act, QLineEdit.LeadingPosition)
            return line

        username_input = make_input("Username", left_icon_unicode="👥")
        password_input = make_input("Password", left_icon_unicode="🔒", echo_mode=QLineEdit.Password)
        confirm_input = make_input("Confirm Password", left_icon_unicode="🔒", echo_mode=QLineEdit.Password)

        eye_btn = QToolButton(confirm_input)
        eye_btn.setCursor(Qt.PointingHandCursor)
        eye_btn.setCheckable(True)
        eye_btn.setFixedSize(22, 22)
        eye_btn.setStyleSheet(f"""
            QToolButton {{
                border: none;
                background: transparent;
                color: {COLOR_PLACEHOLDER};
                font-size: 14px;
            }}
        """)
        eye_btn.setText("👁") 
        eye_btn.move(confirm_input.width() - 30, 10)
        eye_btn.setToolTip("Show / Hide password")

        def toggle_confirm_visibility(checked):
            if checked:
                confirm_input.setEchoMode(QLineEdit.Normal)
            else:
                confirm_input.setEchoMode(QLineEdit.Password)
        eye_btn.toggled.connect(toggle_confirm_visibility)

        def make_field_with_eye(line_edit, eye_button=None):
            w = QWidget()
            h = QHBoxLayout(w)
            h.setContentsMargins(0, 0, 0, 0)
            h.setSpacing(0)
            h.addWidget(line_edit)
            if eye_button:
                holder = QWidget()
                holder_layout = QHBoxLayout(holder)
                holder_layout.setContentsMargins(8, 0, 0, 0)
                holder_layout.addWidget(eye_button, alignment=Qt.AlignVCenter)
                h.addWidget(holder)
            return w

        confirm_with_eye = make_field_with_eye(confirm_input, eye_btn)

        for wid in (username_input, password_input, confirm_with_eye):
            form_layout.addWidget(wid)

        card_layout.addWidget(form_widget, alignment=Qt.AlignHCenter)

        card_layout.addStretch(1)

        create_btn = QPushButton("Create Account")
        create_btn.setCursor(Qt.PointingHandCursor)
        create_btn.setFixedHeight(46)
        create_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLOR_PRIMARY};
                color: {COLOR_FRAME_BG};
                border: none;
                border-radius: 8px;
                font-weight: 700;
                font-size: {BUTTON_FONT_SIZE}px;
            }}
            QPushButton:hover {{
                box-shadow: 0px 6px 18px rgba(47,60,100,0.12);
            }}
            QPushButton:pressed {{
                transform: translateY(1px);
            }}
        """)
        create_container = QWidget()
        cl = QHBoxLayout(create_container)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.addWidget(create_btn)
        cl.setAlignment(create_btn, Qt.AlignHCenter)
        card_layout.addWidget(create_container)

        bottom_row = QWidget()
        bottom_layout = QHBoxLayout(bottom_row)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(10)

        login_btn = QPushButton("Login")
        login_btn.setCursor(Qt.PointingHandCursor)
        login_btn.setFixedHeight(40)
        login_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: 1px solid {COLOR_INPUT_BORDER};
                border-radius: 8px;
                color: {COLOR_MUTED};
                font-weight: 700;
                font-size: {BUTTON_FONT_SIZE}px;
                padding-left: 16px;
                padding-right: 16px;
            }}
            QPushButton:hover {{
                background: rgba(0,0,0,0.02);
            }}
        """)

        bottom_layout.addStretch(1)
        bottom_layout.addWidget(login_btn, alignment=Qt.AlignRight)

        card_layout.addWidget(bottom_row)

        outer_inner = QWidget()
        inner_layout = QHBoxLayout()
        inner_layout.setContentsMargins(0, 0, 0, 0)
        inner_layout.addWidget(container, alignment=Qt.AlignCenter)
        outer_layout.addLayout(inner_layout)
        outer_layout.addStretch(1)

        def on_create():
            print("Create Account clicked")
            print("Username:", username_input.text())
            print("Password:", password_input.text())
            print("Confirm:", confirm_input.text())

        def on_login():
            print("Login clicked - redirect to login (not implemented)")

        create_btn.clicked.connect(on_create)
        login_btn.clicked.connect(on_login)

        self.resizeEvent = self._on_resize

    def _on_resize(self, event):
        w = self.width()
        h = self.height()
        new_w = int(w * 0.65)  
        new_h = int(h * 0.75)
        try:
            self.container.setFixedWidth(new_w)
            self.container.setFixedHeight(new_h)
        except Exception:
            pass
        super(CreateAccountWindow, self).resizeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CreateAccountWindow()
    win.show()
    sys.exit(app.exec())