from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from database import Base


class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    cook_time = Column(Integer)  # Время приготовления
    views = Column(Integer, default=0)  # Количество просмотров
    description = Column(Text)  # Текстовое описание рецепта
     # Аннотация типа для списка ингредиентов
    ingredients: List["Ingredient"] = relationship("Ingredient", back_populates="recipe")


class Ingredient(Base):
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'))

   # Аннотация типа для связи с рецептом
    recipe: Optional["Recipe"] = relationship("Recipe", back_populates="ingredients")
