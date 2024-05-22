import pytest
import asyncio
from bson import ObjectId

@pytest.mark.asyncio(scope="session")
async def test_root(async_client):
    async for client in async_client:
        response = await client.get("/")
        assert response.status_code == 200

# region User
@pytest.mark.skip(reason="Временно отключен")
@pytest.mark.asyncio(scope="session")
async def test_200_create_user(async_client):
    async for client in async_client:
        user_data = {
            "username": "AutotestUser",
            "email": "AutotestUser@mail.ru",
            "password": "AutotestUser"
        }
        response = await client.post("/users", json=user_data)
        data = response.json()
        print(f"{data}")
        assert response.status_code == 200

@pytest.mark.asyncio(scope="session")
async def test_200_get_all_users(async_client):
    async for client in async_client:
        response = await client.get("/users")
        data = response.json()
        print(f"all users: {data}")
        assert response.status_code == 200

# endregion

# region Dish
@pytest.mark.asyncio(scope="session")
async def test_200_get_all_dishes(async_client):
    async for client in async_client:
        response = await client.get("/dishes")
        data = response.json()
        print(f"all dishes: {data}")
        assert response.status_code == 200

@pytest.mark.asyncio(scope="session")
async def test_500_error_create_dish(async_client):
    async for client in async_client:
        dish_data = {
            "name": "TitleDish",
            "description": "DescriptionDish",
            "price": 10.99,
            "created_by": "TestUser"  # Assumes this user does not exist
        }
        response = await client.post("/dishes", json=dish_data)
        assert response.status_code == 500

# @pytest.mark.asyncio(scope="session")
# async def test_404_get_dish(async_client):
#     id_dish = ObjectId()
#     print(id_dish)
#     async for client in async_client:
#         response = await client.get(f"/dishes/{id_dish}")
#         assert response.status_code == 404
# endregion
