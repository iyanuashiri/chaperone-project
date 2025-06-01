from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.security import manager, verify_hashed_password, OAuth2PasswordNewRequestForm
from app import models
from app.api.deps import SessionDep

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login/", status_code=status.HTTP_200_OK)
async def login(session: SessionDep, data: OAuth2PasswordNewRequestForm = Depends()):
    email = data.email
    password = data.password

    user = session.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not correct",
                            headers={"WWW-Authenticate": "Bearer"})

    if not verify_hashed_password(raw_password=password, hashed_password=user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Password not correct",
                            headers={"WWW-Authenticate": "Bearer"})

    access_token = manager.create_access_token(data={"sub": email}, expires=timedelta(hours=12))
    return {"access_token": access_token, "token_type": "bearer", "email": email}
    