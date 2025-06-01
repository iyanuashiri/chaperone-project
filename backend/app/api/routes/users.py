from fastapi import APIRouter, Depends, HTTPException, status

from app import models, schemas
from app.api.deps import SessionDep, manager

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserRead)
async def create_user(user: schemas.UserCreate, session: SessionDep) -> schemas.UserRead:
    existing_user = session.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = models.User(first_name=user.first_name, last_name=user.last_name, email=user.email, password=user.password)
    db_user.set_password(user.password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user  


@router.get("/", response_model=list[schemas.UserRead])
async def get_users(session: SessionDep, ) -> list[schemas.UserRead]:
    users = session.query(models.User).all()
    return users
    
    
@router.get("/{user_id}/", response_model=schemas.UserRead)
async def get_users(user_id: int, session: SessionDep) -> schemas.UserRead:
    user = session.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
