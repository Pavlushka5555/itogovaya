# Этот файл содержит определения схем Pydantic для
# валидации данных и передачи данных
# между клиентом и сервером.
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DishCreate(BaseModel):
    name: str
    description: str
    price: float


class DishUpdate(BaseModel):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]


class DishResponse(BaseModel):
    id: str
    name: str
    description: str
    price: float
    model_config = ConfigDict(from_attributes=True)
