from abc import ABC, abstractmethod
from typing import Optional, List
from models.product import Product
from core.abstracts.base_repository import BaseRepository

class IProductRepository(BaseRepository[Product], ABC):

    @abstractmethod
    def get_by_barcode(self, barcode: str)->Optional[Product]:
        pass