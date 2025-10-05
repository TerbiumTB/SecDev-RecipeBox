class Ingredient:
    def __init__(self, name: str, amount: str):
        self.name = name
        self.amount = amount


class Recipe:
    def __init__(
        self,
        name: str,
        ingredients: list[Ingredient],
        total_time: int,
        description: str,
    ):
        self.name = name
        self.ingredients = ingredients
        self.total_time = total_time
        self.description = description
