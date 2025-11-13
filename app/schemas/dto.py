from pydantic import BaseModel, Field

from app.models.domain import Ingredient, Recipe


class Health(BaseModel):
    status: dict[str, str]


class IngredientIn(BaseModel):
    name: str = Field(..., min_length=1)
    amount: int = Field(..., gt=0)
    units: str = Field(..., min_length=1)

    def to_entity(self) -> Ingredient:
        return Ingredient(**self.model_dump())


class RecipeCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    ingredients: list[IngredientIn]
    total_time: int = Field(..., ge=0)
    description: str = Field(..., min_length=1)


class RecipeUpdate(BaseModel):
    ingredients: list[IngredientIn] | None = None
    total_time: int | None = Field(None, gt=0)
    description: str | None = None


class IngredientOut(BaseModel):
    name: str
    amount: int
    units: str

    # def __init__():
    @classmethod
    def from_entity(self, ingredient: Ingredient):
        return self(**ingredient.__dict__)


class RecipeOut(BaseModel):
    name: str
    ingredients: list[IngredientOut]
    total_time: int
    description: str

    @classmethod
    def from_entity(self, recipe: Recipe):
        return self(
            name=recipe.name,
            ingredients=[
                IngredientOut.from_entity(ingredient) for ingredient in recipe.ingredients
            ],
            total_time=recipe.total_time,
            description=recipe.description,
        )
