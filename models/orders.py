from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId
from datetime import datetime

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')

class OrderCreate(BaseModel):
    user_id: PyObjectId
    dish_ids: List[PyObjectId]
    total_price: float
    order_status: str  # e.g., "pending", "in progress", "completed", "canceled"

class OrderUpdate(BaseModel):
    user_id: Optional[PyObjectId]
    dish_ids: Optional[List[PyObjectId]]
    total_price: Optional[float]
    order_status: Optional[str]

class OrderResponse(BaseModel):
    id: str
    user_id: str
    dish_ids: List[str]
    total_price: float
    order_status: str
    order_time: datetime
    model_config = ConfigDict(from_attributes=True)
