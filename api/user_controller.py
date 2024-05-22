from typing import List
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ReturnDocument

from data_base.database import get_db
from models import UserCreate, UserResponse, UserUpdate
from security.security import get_password_hash
from utils import serialize_model

from logger.logger import log_error

router = APIRouter()


@router.get("/{id}", summary="Получить пользователя по идентификатору", response_model=UserResponse)
async def get(id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        item = await db.users.find_one({"_id": ObjectId(id)})
        return serialize_model(UserResponse, item)
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        log_error(f"Произошла ошибка: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)


@router.get("", summary="Получить всех пользователей", response_model=List[UserResponse])
async def get_all(db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        items = await db.users.find().to_list(1000)
        return [serialize_model(UserResponse, item) for item in items]
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        log_error(f"Произошла ошибка: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)


@router.post("", summary="Создать пользователя", response_model=UserResponse)
async def create(item: UserCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        item.password = get_password_hash(item.password)
        dump = item.model_dump()
        result = await db.users.insert_one(dump)
        created_item = await db.users.find_one({"_id": result.inserted_id})
        return serialize_model(UserResponse, created_item)
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        log_error(f"Произошла ошибка: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)


@router.delete("/{id}", summary="Удалить пользователя", response_model=str)
async def delete(id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        result = await db.users.delete_one({"_id": ObjectId(id)})
        if result.deleted_count > 0:
            return "ok"
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        log_error(f"Произошла ошибка: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)


@router.patch("/{id}", summary="Изменить данные о пользователе", response_model=UserResponse)
async def update(id: str, item: UserUpdate, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        dump = {
            k: v for k, v in item.model_dump(by_alias=True).items() if v is not None
        }
        print(dump)
        updated_item = await db.users.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": dump},
            return_document=ReturnDocument.AFTER,
        )
        if updated_item is None:
            raise HTTPException(status_code=404, detail="Такого пользователя нет")
        return serialize_model(UserResponse, updated_item)
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        log_error(f"Произошла ошибка: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)
