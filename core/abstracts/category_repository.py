from abc import ABC
from models.category import Category
from core.abstracts.base_repository import BaseRepository

class ICategoryRepository(BaseRepository[Category], ABC):
    pass