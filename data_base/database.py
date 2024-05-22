import os
import dotenv
import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorDatabase

dotenv.load_dotenv()

MONGODB_URL = os.getenv("DATABASE_URL")
MONGODB_DATABASE_NAME = os.getenv("DATABASE_NAME")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
mongo_db = client[MONGODB_DATABASE_NAME]


async def get_db() -> AsyncIOMotorDatabase:
    return mongo_db
