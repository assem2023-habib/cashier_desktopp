from enum import Enum

class InvoiceStatus(Enum):
    PENDING= "pending"
    PAID= "paid"
    CANCELLED= "cancelled"