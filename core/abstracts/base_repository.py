from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional

T= TypeVar("T")

class BaseRepository(ABC, Generic[T]):

    @abstractmethod
    def add(self, obj: T)->T:
        pass

    @abstractmethod
    def get(self, obj_id: int)->Optional[T]:
        pass

    @abstractmethod
    def list(self)->List[T]:
        pass

    @abstractmethod
    def update(self, obj: T)-> T:
        pass
    
    @abstractmethod
    def delete(self, obj: T)->bool:
        pass

    @abstractmethod
    def paginate(self,page: int= 1, per_page: int= 10)->List[T]:
        pass