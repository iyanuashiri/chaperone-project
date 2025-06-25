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


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.URLRead])
async def get_urls(session: SessionDep, current_user: models.User = Depends(manager)) -> list[schemas.URLRead]:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")
    urls = session.query(models.URL).filter(models.URL.user_id == current_user.id).all()
    return urls


@router.delete("/{url_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_url(url_id: int, session: SessionDep, current_user: models.User = Depends(manager)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")

    url = session.get(models.URL, url_id)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    session.delete(url)
    session.commit()
    return
