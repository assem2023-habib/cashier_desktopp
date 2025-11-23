from abc import ABC, abstractmethod
from typing import Optional, List
from models.customer import Customer
from core.abstracts.base_repository import BaseRepository

class ICustomerRepository(BaseRepository[Customer], ABC):

    @abstractmethod
    def get_by_name(self, name: str)->Optional[Customer]:
        pass

    @abstractmethod
    def get_by_phone(self, phone: str)->Optional[Customer]:
        pass