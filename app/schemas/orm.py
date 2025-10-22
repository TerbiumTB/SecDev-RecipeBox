from typing import List, Optional

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from app.models import domain


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)


class Recipe(Base):
    __tablename__ = "recipes"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    total_time: Mapped[int] = mapped_column(Integer, nullable=False)

    ingredients: Mapped[List["Ingredient"]] = relationship(
        back_populates="recipe",
        cascade="all, delete-orphan",
        lazy="joined",
    )

    def to_entity(self) -> domain.Recipe:
        return domain.Recipe(
            name=self.name,
            ingredients=[_.to_entity() for _ in self.ingredients],
            total_time=self.total_time,
            description=self.description,
        )

    @classmethod
    def from_entity(self, entity: domain.Recipe) -> "Recipe":
        recipe = self()
        recipe.name = entity.name
        recipe.ingredients = [Ingredient.from_entity(_) for _ in entity.ingredients]
        recipe.total_time = entity.total_time
        recipe.description = entity.description
        return recipe


class Ingredient(Base):
    __tablename__ = "ingredients"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    units: Mapped[str] = mapped_column(String(10), nullable=False)

    recipe_id: Mapped[int] = mapped_column(ForeignKey("recipes.id"), nullable=False)
    recipe: Mapped["Recipe"] = relationship(back_populates="ingredients")

    def to_entity(self) -> domain.Ingredient:
        return domain.Ingredient(self.name, self.amount, self.units)

    @classmethod
    def from_entity(self, entity: domain.Ingredient) -> "Ingredient":
        ingredient = self()
        ingredient.name = entity.name
        ingredient.amount = entity.amount
        ingredient.units = entity.units
        return ingredient
