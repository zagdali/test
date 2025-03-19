from typing import List

from pydantic import BaseModel


class IngredientOut(BaseModel):
    name: str

class BaseRecipe(BaseModel):
    title: str
    cook_time: int  # Время приготовления
    description: str

class RecipeIn(BaseRecipe):
    ingredients: List[str]  # Список ингредиентов в виде строк

class RecipeOut(BaseRecipe):
    id: int
    views: int
    ingredients: List[IngredientOut]

    class Config:
        from_attributes = True
