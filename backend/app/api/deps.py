from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.security import manager
from app.core.database import get_session
from app import models


@manager.user_loader()
async def get_user(email: str = None):
    session = next(get_session())
    return session.query(models.User).filter(models.User.email == email).first()


SessionDep = Annotated[Session, Depends(get_session)] 
