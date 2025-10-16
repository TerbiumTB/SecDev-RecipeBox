from app.models.errors import InternalApiError, NotFoundApiError
from app.models.models import Ingredient, Recipe


class RecipeRepo:
    def __init__(self):
        self._db: dict[str, Recipe] = dict()

    def add(self, recipe: Recipe) -> None:
        if recipe.name in self._db:
            raise InternalApiError(f"Recipe {recipe.name} already exists")
        self._db[recipe.name] = recipe

    def delete(self, name: str) -> None:
        if name not in self._db:
            raise NotFoundApiError(f"Recipe {name} not found")
        del self._db[name]

    def update(
        self,
        name: str,
        ingredients: list[Ingredient] | None = None,
        total_time: int | None = None,
        description: str | None = None,
    ) -> Recipe:
        if name not in self._db:
            raise NotFoundApiError(f"Recipe {name} not found")

        recipe = self._db[name]
        if ingredients is not None:
            recipe.ingredients = ingredients

        if total_time is not None:
            recipe.total_time = total_time

        if description is not None:
            recipe.description = description

        return recipe

    def find(self, name: str) -> Recipe | None:
        return self._db.get(name)

    def all(self) -> list[Recipe]:
        return list(self._db.values())
