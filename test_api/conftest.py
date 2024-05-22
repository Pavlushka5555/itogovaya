import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from main import app


@pytest.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client

# @pytest.fixture(scope="session")
# def loop():
#     loop = asyncio.new_event_loop()
#     yield loop
#     loop.close()
