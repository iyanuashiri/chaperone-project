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
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(api_router, prefix="/api/v1")    




