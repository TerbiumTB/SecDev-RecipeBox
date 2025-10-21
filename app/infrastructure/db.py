from sqlalchemy import select
from sqlalchemy.orm import Session

from app.infrastructure.repo import IRecipeRepo
from app.models.errors import NotFoundApiError
from app.models.models import Ingredient, Recipe
from app.schemas import orm


class RecipeDB(IRecipeRepo):
    def __init__(self, session: Session):
        self.session = session

    def add(self, recipe: Recipe) -> None:
        self.session.add(orm.Recipe.from_entity(recipe))
        self.session.commit()

    def delete(self, name: str) -> None:
        recipe = (
            self.session.execute(select(orm.Recipe).where(orm.Recipe.name == name))
            .unique()
            .scalar_one_or_none()
        )
        if not recipe:
            raise NotFoundApiError(f"Recipe {name} not found")

        self.session.delete(recipe)
        self.session.commit()

    def update(
        self,
        name: str,
        ingredients: list[Ingredient] | None = None,
        total_time: int | None = None,
        description: str | None = None,
    ) -> Recipe:
        recipe = (
            self.session.execute(select(orm.Recipe).where(orm.Recipe.name == name))
            .unique()
            .scalar_one_or_none()
        )
        if not recipe:
            raise NotFoundApiError(f"Recipe {name} not found")

        if ingredients is not None:
            recipe.ingredients = ingredients
        if total_time is not None:
            recipe.total_time = total_time
        if description is not None:
            recipe.description = description

        self.session.commit()
        self.session.refresh(recipe)
        return recipe.to_entity()

    def find(self, name: str) -> Recipe | None:
        recipe = (
            self.session.execute(select(orm.Recipe).where(orm.Recipe.name == name))
            .unique()
            .scalar_one_or_none()
        )
        if recipe:
            return recipe.to_entity()
        return None

    def all(self) -> list[Recipe]:
        recipes = list(
            self.session.execute(select(orm.Recipe)).unique().scalars().all()
        )
        return [*map(orm.Recipe.to_entity, recipes)]
