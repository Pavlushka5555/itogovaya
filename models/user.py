# Этот файл содержит определения схем Pydantic для
# валидации данных и передачи данных
# между клиентом и сервером.
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[str]


class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    password: str
    model_config = ConfigDict(from_attributes=True)
