from fastapi import APIRouter, HTTPException, status

from app.schemas import schemas
from app.api.deps import SessionDep
from app.crud import get_user_by_email, create_user as crud_create_user, list_users, get_user_by_id

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserRead)
async def create_user(user: schemas.UserCreate, session: SessionDep) -> schemas.UserRead:
    existing_user = get_user_by_email(session, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud_create_user(session, user)


@router.get("/", response_model=list[schemas.UserRead])
async def get_users(session: SessionDep) -> list[schemas.UserRead]:
    return list_users(session)


@router.get("/{user_id}/", response_model=schemas.UserRead)
async def get_users(user_id: int, session: SessionDep) -> schemas.UserRead:
    user = get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
