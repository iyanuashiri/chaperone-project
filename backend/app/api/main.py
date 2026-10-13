from fastapi import APIRouter

from app.api.routes import associations, vocabularies, users, login, urls, quizzes, game, stats

api_router = APIRouter()

api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(vocabularies.router)
api_router.include_router(associations.router)
api_router.include_router(urls.router)
api_router.include_router(quizzes.router)
api_router.include_router(game.router)
api_router.include_router(stats.router)
