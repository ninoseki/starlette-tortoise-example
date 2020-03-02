from starlette.config import environ
from starlette.testclient import TestClient
from tortoise import Tortoise, run_async
from tortoise.contrib.test import finalizer, initializer
import os
import pytest

from app import settings
from app import create_app
from app.models import Users

@pytest.fixture(scope="session", autouse=True)
def initialize_tests(request):
    db_url = environ.get("TORTOISE_TEST_DB", "sqlite://:memory:")
    initializer(settings.APP_MODELS, db_url=db_url)
    request.addfinalizer(finalizer)


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


@pytest.fixture
async def users(request):
    pass
