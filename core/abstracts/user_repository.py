from abc import ABC, abstractmethod
from typing import Optional, List
from models.user import User
from core.abstracts.base_repository import BaseRepository

class IUserRepository(BaseRepository[User], ABC):

    @abstractmethod
    def get_by_username(self, user_name: str)->Optional[User]:
        pass

    @abstractmethod
    def authenticate(self, user_name: str, password: str)-> Optional[User]:
        pass