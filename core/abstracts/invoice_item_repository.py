from abc import ABC, abstractmethod
from typing import  List
from models.invoice_item import InvoiceItem
from core.abstracts.base_repository import BaseRepository

class IInvoiceItemRepository(BaseRepository[InvoiceItem], ABC):

    @abstractmethod
    def list_by_invoice_id(self, invoice_id: int)->List[InvoiceItem]:
        pass