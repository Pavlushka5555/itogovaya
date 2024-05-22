from typing import List
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ReturnDocument
from data_base.database import get_db
from models import OrderCreate, OrderResponse, OrderUpdate
from utils import serialize_model
from logger.logger import log_error

router = APIRouter()


@router.get("/{id}", summary="Получить заказ по идентификатору", response_model=OrderResponse)
async def get_order(id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        item = await db.orders.find_one({"_id": ObjectId(id)})
        if item is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Заказ не найден")
        return serialize_model(OrderResponse, item)
    except Exception as e:
        error_message = f"Произошла ошибка: {str(e)}"
        log_error(error_message)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)


@router.get("", summary="Получить все заказы", response_model=List[OrderResponse])
async def get_all_orders(db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        items = await db.orders.find().to_list(1000)
        return [serialize_model(OrderResponse, item) for item in items]
    except Exception as e:
        error_message = f"Произошла ошибка: {str(e)}"
        log_error(error_message)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)


@router.post("", summary="Создать заказ", response_model=OrderResponse)
async def create_order(order: OrderCreate, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        order_doc = order.dict()
        order_doc["order_time"] = datetime.now()
        result = await db.orders.insert_one(order_doc)
        created_order = await db.orders.find_one({"_id": result.inserted_id})
        return serialize_model(OrderResponse, created_order)
    except Exception as e:
        error_message = f"Произошла ошибка: {str(e)}"
        log_error(error_message)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)


@router.delete("/{id}", summary="Удалить заказ", response_model=str)
async def delete_order(id: str, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        result = await db.orders.delete_one({"_id": ObjectId(id)})
        if result.deleted_count > 0:
            return "ok"
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Заказ не найден")
    except Exception as e:
        error_message = f"Произошла ошибка: {str(e)}"
        log_error(error_message)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)


@router.patch("/{id}", summary="Обновить заказ", response_model=OrderResponse)
async def update_order(id: str, order: OrderUpdate, db: AsyncIOMotorDatabase = Depends(get_db)):
    try:
        update_data = {
            k: v for k, v in order.dict(by_alias=True).items() if v is not None
        }
        updated_order = await db.orders.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": update_data},
            return_document=ReturnDocument.AFTER,
        )
        if updated_order is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Заказ не найден")
        return serialize_model(OrderResponse, updated_order)
    except Exception as e:
        error_message = f"Произошла ошибка: {str(e)}"
        log_error(error_message)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=error_message)
