from json import JSONDecodeError
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from tortoise import Tortoise
import logging

from app.models import Users
from app import settings

# logging.basicConfig(level=logging.DEBUG)


async def list_all(_: Request) -> JSONResponse:
    users = await Users.all()
    return JSONResponse({"users": [str(user) for user in users]})

routes = [
    Route('/', list_all),
]


def create_app():
    return Starlette(
        debug=settings.DEBUG,
        routes=routes
    )


app = create_app()


@app.on_event("startup")
async def on_startup() -> None:
    await Tortoise.init(
        db_url=settings.DATABASE_URL, modules={"models": settings.APP_MODELS}
    )
    await Tortoise.generate_schemas()


@app.on_event("shutdown")
async def on_shutdown() -> None:
    await Tortoise.close_connections()
