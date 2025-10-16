from app.infrastructure.db import RecipeRepo
from app.models.errors import NotFoundApiError
from app.models.models import Ingredient, Recipe


class RecipeService:
    def __init__(self, repo: RecipeRepo):
        self.repo = repo

    def create_recipe(
        self,
        name: str,
        ingredients: list[Ingredient],
        total_time: int,
        description: str,
    ) -> Recipe:

        recipe = Recipe(name, ingredients, total_time, description)
        self.repo.add(recipe)
        return recipe

    def get_recipe_by_name(self, name: str) -> Recipe:
        recipe = self.repo.find(name)

        if not recipe:
            raise NotFoundApiError(f"Recipe {name} not found")

        return recipe

    def update_recipe(
        self,
        name: str,
        ingredients: list[Ingredient] | None = None,
        total_time: int | None = None,
        description: str | None = None,
    ) -> Recipe:

        return self.repo.update(
            name,
            ingredients=ingredients,
            total_time=total_time,
            description=description,
        )

    def delete_recipe(self, name: str) -> None:
        self.repo.delete(name)

    def all_recipes(self) -> list[Recipe]:
        return self.repo.all()
