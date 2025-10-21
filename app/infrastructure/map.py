from app.infrastructure.repo import IRecipeRepo
from app.models.errors import InternalApiError, NotFoundApiError
from app.models.models import Ingredient, Recipe


class RecipeMap(IRecipeRepo):
    def __init__(self):
        self.map: dict[str, Recipe] = dict()

    def add(self, recipe: Recipe) -> None:
        if recipe.name in self.map:
            raise InternalApiError(f"Recipe {recipe.name} already exists")
        self.map[recipe.name] = recipe

    def delete(self, name: str) -> None:
        if name not in self.map:
            raise NotFoundApiError(f"Recipe {name} not found")
        del self.map[name]

    def update(
        self,
        name: str,
        ingredients: list[Ingredient] | None = None,
        total_time: int | None = None,
        description: str | None = None,
    ) -> Recipe:
        if name not in self.map:
            raise NotFoundApiError(f"Recipe {name} not found")

        recipe = self.map[name]
        if ingredients is not None:
            recipe.ingredients = ingredients

        if total_time is not None:
            recipe.total_time = total_time

        if description is not None:
            recipe.description = description

        return recipe

    def find(self, name: str) -> Recipe | None:
        return self.map.get(name)

    def all(self) -> list[Recipe]:
        return list(self.map.values())
