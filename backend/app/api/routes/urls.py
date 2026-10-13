from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas import schemas
from app.api.deps import manager, SessionDep
from app.helpers import get_url_title_and_description
from app.models import models
from app.crud import create_url, list_urls, get_url, delete_url

router = APIRouter(prefix="/urls", tags=["URLs"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.URLRead)
async def create_url(url: schemas.URLCreate, session: SessionDep, current_user: models.User = Depends(manager)) -> schemas.URLRead:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")

    title, description = get_url_title_and_description(url.url)
    return create_url(session, current_user.id, url, title, description)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.URLRead])
async def get_urls(session: SessionDep, current_user: models.User = Depends(manager)) -> list[schemas.URLRead]:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")
    return list_urls(session, current_user.id)


@router.delete("/{url_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_url(url_id: int, session: SessionDep, current_user: models.User = Depends(manager)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")

    url = get_url(session, url_id, current_user.id)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")
    delete_url(session, url)
    return
