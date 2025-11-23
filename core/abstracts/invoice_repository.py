from abc import ABC, abstractmethod
from typing import Optional, List
from models.invoice import Invoice
from core.abstracts.base_repository import BaseRepository
from datetime import date

class IInvoiceRepository(BaseRepository[Invoice], ABC):

    @abstractmethod
    def list_by_date_range(self, start: date, end: date)->list[Invoice]:
        pass