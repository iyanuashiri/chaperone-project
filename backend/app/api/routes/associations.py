from fastapi import APIRouter, Depends, HTTPException, status

from app import models, schemas
from app.prompts import generate_associations
from app.api.deps import SessionDep, manager

router = APIRouter(prefix="/associations", tags=["Associations"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.AssociationRead)
async def create_association(association: schemas.AssociationCreate, session: SessionDep, current_user: models.User = Depends(manager)) -> schemas.AssociationRead:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")

    vocab = session.get(models.Vocabulary, association.vocabulary_id)
    if not vocab:
        raise HTTPException(status_code=404, detail="Vocabulary not found")

    generated_associations = await generate_associations(vocabulary=vocab.word, number_of_options=3)
    generated_associations = generated_associations[0]
    print(generated_associations)

    db_association = models.Association(user_id=current_user.id, vocabulary_id=vocab.id)
    session.add(db_association)
    session.commit()
    session.refresh(db_association)
    
    for option, meaning in generated_associations['options'].items():
        if option.isupper():
            is_correct = True
        else:
            is_correct = False
        db_option = models.Option(option=option, meaning=meaning, is_correct=is_correct, association_id=db_association.id)
        session.add(db_option)
        session.commit()
        session.refresh(db_option)

    return db_association


@router.get("/", response_model=list[schemas.AssociationRead])
async def get_associations(session: SessionDep, current_user: models.User = Depends(manager)) -> list[schemas.AssociationRead]:
    """Get all associations for the current user"""
    associations = session.query(models.Association).order_by(
        models.Association.id.desc()
    ).filter(
        models.Association.user_id == current_user.id
    ).all()
    return associations


@router.get("/{association_id}", response_model=schemas.AssociationRead)
async def get_association(association_id: int, session: SessionDep, current_user: models.User = Depends(manager)) -> schemas.AssociationRead:
    """Get a specific association by ID"""
    association = session.query(models.Association).filter(
        models.Association.id == association_id,
        models.Association.user_id == current_user.id
    ).first()
    
    if not association:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Association not found"
        )
    
    return association


@router.put("/{association_id}/correct", response_model=schemas.AssociationRead)
async def update_association(association_id: int, session: SessionDep, current_user: models.User = Depends(manager)) -> schemas.AssociationRead:
    """Update a specific association by ID"""
    association = session.query(models.Association).filter(
        models.Association.id == association_id,
        models.Association.user_id == current_user.id
    ).first()
    
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
    association = session.query(models.Association).filter(
        models.Association.id == association_id,
        models.Association.user_id == current_user.id
    ).first()
    
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
