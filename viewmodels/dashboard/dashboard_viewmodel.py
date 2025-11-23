from PySide6.QtCore import QObject, Signal, Slot, Property

class DashboardViewModel(QObject):
    def __init__(self):
        super().__init__()
        # Mock Data for now
        self._daily_sales = "$1,500"
        self._receipts_count = "125"
        self._avg_receipt_value = "$12.00"
        self._low_stock_count = "15"

    @Property(str, constant=True)
    def dailySales(self):
        return self._daily_sales

    @Property(str, constant=True)
    def receiptsCount(self):
        return self._receipts_count

    @Property(str, constant=True)
    def avgReceiptValue(self):
        return self._avg_receipt_value

    @Property(str, constant=True)
    def lowStockCount(self):
        return self._low_stock_count

    logoutRequested = Signal()

    @Slot()
    def logout(self):
        # Perform any cleanup or session clearing here if needed
        self.logoutRequested.emit()
