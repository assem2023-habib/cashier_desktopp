from PySide6.QtWidgets import QPushButton, QGraphicsDropShadowEffect
from PySide6.QtGui import QColor
from PySide6.QtCore import QSize, QPropertyAnimation, QEasingCurve, Property, QRect, Qt

class PrimaryButton(QPushButton):
    def __init__(
            self,
            text: str = "",
            color: str = "#2F3C64",
            text_color: str = "#FFFFFF",
            hover_color: str = "#3E4C7A",
            fixed_size: QSize = QSize(180, 42),
            pressed_backgroundColor: str = "#222222",
            disabled_backgroundColor: str = "#6E6E6E",
            disabled_color: str = "#CFCFCF",
            parent=None
            ):
        super().__init__(text, parent)

        self._base_color = QColor(color)
        self._hover_color = QColor(hover_color)
        self._current_color = self._base_color
        self._text_color = text_color

        self._fixed_size = fixed_size if fixed_size is not None else QSize(180, 42)

        self.pressed_backgroundColor = pressed_backgroundColor
        self.disabled_backgroundColor = disabled_backgroundColor
        self.disabled_color = disabled_color

        self._animation = None

        self._setup_ui()
    
    def getColor(self):
        return self._current_color

    def setColor(self, color):
        self._current_color = color
        self._apply_style()

    colorProp = Property(QColor, getColor, setColor)
    def _setup_ui(self):
        self.setFixedSize(self._fixed_size)
        self._apply_style()

    def _apply_style(self):
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self._current_color.name()};
                color: {self._text_color};
                border: none;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
                font-weight: 600;
            }}
            QPushButton:pressed {{
                background-color: {self.pressed_backgroundColor};
            }}
            QPushButton:disabled {{
                background-color: {self.disabled_backgroundColor};
                color: {self.disabled_color};
            }}
        """)
    def setDisabled(self, disabled):
        super().setDisabled(disabled)
        if disabled and self._animation:
            self._animation.stop()
    
    def enterEvent(self, event):
        self.animate_color(self._hover_color)
        self.setCursor(Qt.PointingHandCursor)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 130))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)

        super().enterEvent(event)

    def leaveEvent(self, event):
        self.animate_color(self._base_color)
        self.setGraphicsEffect(None)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if not self.isEnabled():
            return super().mousePressEvent(event)

        self._original_geometry = self.geometry()

        shrink_w = int(self.width() * 0.95)
        shrink_h = int(self.height() * 0.95)
        dx = (self.width() - shrink_w) // 2
        dy = (self.height() - shrink_h) // 2

        target_rect = QRect(
            self.x() + dx,
            self.y() + dy,
            shrink_w,
            shrink_h
        )

        anim = QPropertyAnimation(self, b"geometry")
        anim.setDuration(100)
        anim.setEasingCurve(QEasingCurve.OutCubic)
        anim.setStartValue(self.geometry())
        anim.setEndValue(target_rect)
        anim.start()

        self._press_anim = anim

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if hasattr(self, "_original_geometry"):
            anim = QPropertyAnimation(self, b"geometry")
            anim.setDuration(100)
            anim.setEasingCurve(QEasingCurve.OutCubic)
            anim.setStartValue(self.geometry())
            anim.setEndValue(self._original_geometry)
            anim.start()

            self._release_anim = anim

        super().mouseReleaseEvent(event)

    def animate_color(self, target_color: QColor):
        if self._animation:
            self._animation.stop()

        self._animation = QPropertyAnimation(self, b"colorProp")
        self._animation.setDuration(230)
        self._animation.setStartValue(self._current_color)
        self._animation.setEndValue(target_color)
        self._animation.setEasingCurve(QEasingCurve.InOutQuad)
        self._animation.start()

        