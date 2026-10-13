from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas import schemas
from app.prompts.prompts import generate_associations
from app.api.deps import SessionDep, manager
from app.models import models
from app.crud import (
    get_vocabulary,
    create_association,
    create_option,
    get_association,
    list_associations,
)

router = APIRouter(prefix="/associations", tags=["Associations"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.AssociationRead)
async def create_association(association: schemas.AssociationCreate, session: SessionDep, current_user: models.User = Depends(manager)) -> schemas.AssociationRead:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")

    vocab = get_vocabulary(session, association.vocabulary_id)
    if not vocab:
        raise HTTPException(status_code=404, detail="Vocabulary not found")

    generated_associations = await generate_associations(vocabulary=vocab.word, number_of_options=3)
    generated_associations = generated_associations[0]
    print(generated_associations)

    db_association = create_association(session, current_user.id, vocab.id)

    for option, meaning in generated_associations['options'].items():
        is_correct = option.isupper()
        create_option(session, db_association.id, option, meaning, is_correct)

    return db_association


@router.get("/", response_model=list[schemas.AssociationRead])
async def get_associations(session: SessionDep, current_user: models.User = Depends(manager)) -> list[schemas.AssociationRead]:
    """Get all associations for the current user"""
    return list_associations(session, current_user.id)


@router.get("/{association_id}", response_model=schemas.AssociationRead)
async def get_association(association_id: int, session: SessionDep, current_user: models.User = Depends(manager)) -> schemas.AssociationRead:
    """Get a specific association by ID"""
    association = get_association(session, association_id, current_user.id)
    if not association:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Association not found"
        )
    return association


@router.put("/{association_id}/correct", response_model=schemas.AssociationRead)
async def update_association(association_id: int, session: SessionDep, current_user: models.User = Depends(manager)) -> schemas.AssociationRead:
    """Update a specific association by ID"""
    association = get_association(session, association_id, current_user.id)
    if not association:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Association not found"
        )

    association.correct_option()
    session.add(association)
    session.commit()
    session.refresh(association)
    return association


@router.put("/{association_id}/incorrect", response_model=schemas.AssociationRead)
async def update_association(association_id: int, session: SessionDep, current_user: models.User = Depends(manager)) -> schemas.AssociationRead:
    """Update a specific association by ID"""
    association = get_association(session, association_id, current_user.id)
    if not association:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Association not found"
        )

    association.incorrect_option()
    session.add(association)
    session.commit()
    session.refresh(association)
    return association
