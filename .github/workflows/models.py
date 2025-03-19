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
    ingredients = relationship("Ingredient", back_populates="recipe")


class Ingredient(Base):
    __tablename__ = 'ingredients'
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    recipe_id = Column(Integer, ForeignKey('recipes.id'))

    recipe = relationship("Recipe", back_populates="ingredients")


# Первый экран: таблица со списком всех рецептов в базе. Поля в таблице:
#

# Рецепты отсортированы по количеству просмотров — тому, сколько раз открыли детальный рецепт. Чем чаще открывают рецепт, тем он популярнее. Если число просмотров совпадает, рецепты сортируются по времени приготовления.
#
# Второй экран — детальная информация по каждому рецепту:
#
# название блюда,
# время приготовления,
# список ингредиентов,
# текстовое описание.