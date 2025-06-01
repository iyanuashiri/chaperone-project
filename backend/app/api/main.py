from fastapi import APIRouter

from app.api.routes import associations, vocabularies, users, login

api_router = APIRouter()

api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(vocabularies.router)
api_router.include_router(associations.router)
