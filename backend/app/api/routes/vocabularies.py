from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas import schemas
from app.api.deps import manager, SessionDep
from app.models import models
from app.crud import (
    create_vocabulary,
    list_vocabularies,
    get_vocabulary,
)

router = APIRouter(prefix="/vocabularies", tags=["Vocabularies"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.VocabularyRead)
async def create_vocabulary(vocab: schemas.VocabularyCreate, session: SessionDep, current_user: models.User = Depends(manager)) -> schemas.VocabularyRead:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")

    return create_vocabulary(session, vocab)


@router.get("/", response_model=list[schemas.VocabularyRead])
async def get_vocabularies(session: SessionDep, current_user: models.User = Depends(manager)) -> list[schemas.VocabularyRead]:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")
    return list_vocabularies(session)


@router.get("/{vocab_id}/", response_model=schemas.VocabularyRead)
async def get_vocabulary_by_id(vocab_id: int, session: SessionDep, current_user: models.User = Depends(manager)) -> schemas.VocabularyRead:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")

    vocab = get_vocabulary(session, vocab_id)
    if not vocab:
        raise HTTPException(status_code=404, detail="Vocabulary not found")
    return vocab
