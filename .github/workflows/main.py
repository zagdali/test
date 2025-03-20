from typing import List

from fastapi import FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
 
import models
import schemas
from database import async_session_maker, engine


# Обработчики событий через lifespan
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan,title="Кулинарная книга API",
    description="API для управления рецептами: создание, просмотр и список рецептов")

# POST: Создание нового рецепта
@app.post('/recipes/', response_model=schemas.RecipeOut, summary="Создать новый рецепт")
async def create_recipe(recipe: schemas.RecipeIn):
    async with async_session_maker() as db_session:
        new_recipe = models.Recipe(
            title=recipe.title,
            cook_time=recipe.cook_time,
            description=recipe.description
        )

        db_session.add(new_recipe)
        await db_session.commit()
        await db_session.refresh(new_recipe)

        # Добавляем ингредиенты
        for ingredient_name in recipe.ingredients:
            ingredient = models.Ingredient(name=ingredient_name, recipe_id=new_recipe.id)
            db_session.add(ingredient)

        await db_session.commit()
        return new_recipe


# GET: Получение списка всех рецептов
@app.get('/recipes/', response_model=List[schemas.RecipeOut], summary="Получить список всех рецептов")
async def get_recipes():
    async with async_session_maker() as db_session:
        res = await db_session.execute(
            select(models.Recipe).options(selectinload(models.Recipe.ingredients))
            .order_by(models.Recipe.views.desc(), models.Recipe.cook_time)
        )
        return res.scalars().all()


# GET: Получение конкретного рецепта по ID
@app.get('/recipes/{recipe_id}', response_model=schemas.RecipeOut, summary="Получить детальный рецепт")
async def get_recipe(recipe_id: int):
    async with async_session_maker() as db_session:
        res = await db_session.execute(
            select(models.Recipe)
            .where(models.Recipe.id == recipe_id)
            .options(selectinload(models.Recipe.ingredients))
        )
        recipe = res.scalar_one_or_none()

        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")

        # Увеличиваем количество просмотров
        recipe.views += 1
        await db_session.commit()

        return recipe
