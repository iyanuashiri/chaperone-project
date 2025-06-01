from fastapi import APIRouter, Depends, HTTPException, status

from app import models, schemas
from app.api.deps import manager, SessionDep

router = APIRouter(prefix="/vocabularies", tags=["Vocabularies"])



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.VocabularyRead)
async def create_vocabulary(vocab: schemas.VocabularyCreate, session: SessionDep, current_user: models.User = Depends(manager)) -> schemas.VocabularyRead:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")

    db_vocab = models.Vocabulary(word=vocab.word, meaning=vocab.meaning)
    session.add(db_vocab)
    session.commit()
    session.refresh(db_vocab)
    return db_vocab


@router.get("/", response_model=list[schemas.VocabularyRead])
async def get_vocabularies(session: SessionDep, current_user: models.User = Depends(manager)) -> list[schemas.VocabularyRead]:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")
    vocabularies = session.query(models.Vocabulary).all()
    return vocabularies


@router.get("/{vocab_id}/", response_model=schemas.VocabularyRead)
async def get_vocabulary_by_id(vocab_id: int, session: SessionDep, current_user: models.User = Depends(manager)) -> schemas.VocabularyRead:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")
        
    vocab = session.get(models.Vocabulary, vocab_id)
    if not vocab:
        raise HTTPException(status_code=404, detail="Vocabulary not found")
    return vocab
