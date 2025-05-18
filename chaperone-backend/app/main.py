from typing import Annotated
from datetime import timedelta

from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import models
from . import schemas
from app.core.database import create_db_and_tables, get_session
from app.core.security import generate_hashed_password, verify_hashed_password, manager, OAuth2PasswordNewRequestForm
from app.prompts import generate_associations


SessionDep = Annotated[Session, Depends(get_session)] 


app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@manager.user_loader()
async def get_user(email: str = None):
    session = next(get_session())
    return session.query(models.User).filter(models.User.email == email).first()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/login/", status_code=status.HTTP_200_OK)
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
    
    
@app.post("/users/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserRead)
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


@app.get("/users/", response_model=list[schemas.UserRead])
async def get_users(session: SessionDep, ) -> list[schemas.UserRead]:
    users = session.query(models.User).all()
    return users
    
    
@app.get("/users/{user_id}/", response_model=schemas.UserRead)
async def get_users(user_id: int, session: SessionDep) -> schemas.UserRead:
    user = session.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/vocabularies/", status_code=status.HTTP_201_CREATED, response_model=schemas.VocabularyRead)
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


@app.get("/vocabularies/", response_model=list[schemas.VocabularyRead])
async def get_vocabularies(session: SessionDep, current_user: models.User = Depends(manager)) -> list[schemas.VocabularyRead]:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")
    vocabularies = session.query(models.Vocabulary).all()
    return vocabularies


@app.get("/vocabularies/{vocab_id}/", response_model=schemas.VocabularyRead)
async def get_vocabulary_by_id(vocab_id: int, session: SessionDep, current_user: models.User = Depends(manager)) -> schemas.VocabularyRead:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")
        
    vocab = session.get(models.Vocabulary, vocab_id)
    if not vocab:
        raise HTTPException(status_code=404, detail="Vocabulary not found")
    return vocab


@app.post("/associations/", status_code=status.HTTP_201_CREATED, response_model=schemas.AssociationRead)
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


@app.get("/associations/", response_model=list[schemas.AssociationRead])
async def get_associations(session: SessionDep, current_user: models.User = Depends(manager)) -> list[schemas.AssociationRead]:
    """Get all associations for the current user"""
    associations = session.query(models.Association).order_by(
        models.Association.id.desc()
    ).filter(
        models.Association.user_id == current_user.id
    ).all()
    return associations


@app.get("/associations/{association_id}", response_model=schemas.AssociationRead)
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


@app.put("/associations/{association_id}/correct", response_model=schemas.AssociationRead)
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


@app.put("/associations/{association_id}/incorrect", response_model=schemas.AssociationRead)
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
