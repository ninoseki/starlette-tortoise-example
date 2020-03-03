import json
import pytest

from app.models import Users


@pytest.mark.asyncio
async def test_list_all(client, tortoise_db):
    response = await client.get("/")
    assert response.status_code == 200

    data = response.json()
    users = data.get("users", {})
    assert len(users) == 0


@pytest.mark.asyncio
async def test_list_all_with_users(client, tortoise_db):
    await Users.create(username="foo")
    await Users.create(username="bar")

    response = await client.get("/")
    assert response.status_code == 200

    data = response.json()
    users = data.get("users", {})
    assert len(users) == 2
