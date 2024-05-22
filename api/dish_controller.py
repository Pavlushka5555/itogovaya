from typing import List

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ReturnDocument
from data_base.database import get_db
from models import DishCreate, DishResponse, DishUpdate
from utils import serialize_model

from logger.logger import log_error

router = APIRouter()


@router.get("/{id}", summary="Получить блюдо по идентификатору", response_model=DishResponse)
async def get_dish(id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        item = await db.dishes.find_one({"_id": ObjectId(id)})
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Блюдо не найдено")
        return serialize_model(DishResponse, item)
    except Exception as e:
        error_message = f"Произошла ошибка: {str(e)}"
        log_error(error_message)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)


@router.get("", summary="Получить все блюда", response_model=List[DishResponse])
async def get_all_dishes(db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        items = await db.dishes.find().to_list(1000)
        return [serialize_model(DishResponse, item) for item in items]
    except Exception as e:
        error_message = f"Произошла ошибка: {str(e)}"
        log_error(error_message)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)


@router.post("", summary="Создать блюдо", response_model=DishResponse)
async def create_dish(dish: DishCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        if await db.users.find_one({'_id': ObjectId(dish.created_by)}) is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого пользователя нет")
        dish_doc = dish.dict()
        dish_doc["deleted"] = False
        result = await db.dishes.insert_one(dish_doc)
        created_dish = await db.dishes.find_one({"_id": result.inserted_id})
        return serialize_model(DishResponse, created_dish)
    except HTTPException as e:
        log_error(f"Произошла ошибка: {str(e)}")
        raise e
    except Exception as e:
        error_message = f"Произошла ошибка: {str(e)}"
        log_error(error_message)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)


@router.delete("/{id}", summary="Удалить блюдо", response_model=str)
async def delete_dish(id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        updated_dish = await db.dishes.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": {'deleted': True}},
            return_document=ReturnDocument.AFTER,
        )
        if updated_dish is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Блюдо не найдено")
        return "ok"
    except Exception as e:
        error_message = f"Произошла ошибка: {str(e)}"
        log_error(error_message)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)


@router.patch("/{id}", summary="Изменить данные о блюде", response_model=DishResponse)
async def update_dish(id: str, dish: DishUpdate, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        if dish.created_by and (await db.users.find_one({'_id': ObjectId(dish.created_by)}) is None):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого пользователя нет")
        update_data = {k: v for k, v in dish.dict(by_alias=True).items() if v is not None}
        updated_dish = await db.dishes.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": update_data},
            return_document=ReturnDocument.AFTER,
        )
        if updated_dish is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Блюдо не найдено")
        return serialize_model(DishResponse, updated_dish)
    except Exception as e:
        error_message = f"Произошла ошибка: {str(e)}"
        log_error(error_message)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)
