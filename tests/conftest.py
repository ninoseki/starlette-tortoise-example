from starlette.config import environ
from tortoise import Tortoise
from tortoise.exceptions import DBConnectionError
import asyncio
import httpx
import pytest

from app import create_app
from app import settings


@pytest.fixture(scope="module")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture
async def client():
    app = create_app()
    return httpx.AsyncClient(app=app, base_url="http://testserver")


@pytest.fixture
async def tortoise_db():
    db_url = environ.get("TORTOISE_TEST_DB", "sqlite://:memory:")
    try:
        await Tortoise.init(db_url=db_url, modules={"models": settings.APP_MODELS})
        await Tortoise._drop_databases()
    except DBConnectionError:
        pass

    await Tortoise.init(db_url=db_url, modules={"models": settings.APP_MODELS})
    await Tortoise.generate_schemas()

    yield

    await Tortoise.close_connections()
