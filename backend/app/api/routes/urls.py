from fastapi import APIRouter, Depends, HTTPException, status

from app import models, schemas
from app.api.deps import manager, SessionDep
from app.helpers import get_url_title_and_description

router = APIRouter(prefix="/urls", tags=["URLs"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.URLRead)
async def create_url(url: schemas.URLCreate, session: SessionDep, current_user: models.User = Depends(manager)) -> schemas.URLRead:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")

    title, description = get_url_title_and_description(url.url)
    db_url = models.URL(url=url.url, title=title, description=description, user_id=current_user.id)
    session.add(db_url)
    session.commit()
    session.refresh(db_url)
    return db_url
