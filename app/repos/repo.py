from abc import ABC, abstractmethod

from app.models.domain import Ingredient, Recipe


class IRecipeRepo(ABC):
    @abstractmethod
    def add(self, recipe: Recipe) -> None:
        pass

    @abstractmethod
    def delete(self, name: str) -> None:
        pass

    @abstractmethod
    def update(
        self,
        name: str,
        ingredients: list[Ingredient] | None = None,
        total_time: int | None = None,
        description: str | None = None,
    ) -> Recipe:
        pass

    @abstractmethod
    def find(self, name: str) -> Recipe | None:
        pass

    @abstractmethod
    def all(self) -> list[Recipe]:
        pass
