from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import create_db_and_tables
from app.api.main import api_router


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    title="Chaperone API",
    description="Chaperone API",
    version="1.0.0",
    openapi_url="/openapi.json",
    generate_unique_id=custom_generate_unique_id,
)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

# Also allow extension origins (moz-extension://, chrome-extension://) and any
# localhost dev port via allow_origin_regex below.

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^(https?://(localhost|127\.0\.0\.1)(:\d+)?|moz-extension://.*|chrome-extension://.*)$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(api_router, prefix="/api/v1")    




