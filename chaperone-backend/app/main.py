from typing import Annotated
from datetime import timedelta

from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from . import models
from . import schemas
from app.core.database import create_db_and_tables, get_session
from app.core.security import generate_hashed_password, verify_hashed_password, manager, OAuth2PasswordNewRequestForm
from app.prompts import generate_associations


SessionDep = Annotated[Session, Depends(get_session)] 


app = FastAPI()

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
    
    
@app.post("/users/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserBase)
async def create_user(user: models.User, session: SessionDep) -> models.User:
    existing_user = session.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = models.User.model_validate(user)
    db_user.password = generate_hashed_password(raw_password=user.password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user  


@app.get("/users/", response_model=list[schemas.UserBase])
async def get_users(session: SessionDep, ) -> list[models.User]:
    users = session.query(models.User).all()
    return users
    
    
@app.get("/users/{user_id}/", response_model=schemas.UserBase)
async def get_users(user_id: int, session: SessionDep) -> models.User:
    user = session.get(models.User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.post("/vocabularies/", status_code=status.HTTP_201_CREATED, response_model=schemas.VocabularyRead)
async def create_vocabulary(vocab: schemas.VocabularyCreate, session: SessionDep, current_user: models.User = Depends(manager)) -> models.Vocabulary:
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
async def get_vocabularies(session: SessionDep, current_user: models.User = Depends(manager)) -> list[models.Vocabulary]:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")
    vocabularies = session.query(models.Vocabulary).all()
    return vocabularies


@app.get("/vocabularies/{vocab_id}/", response_model=schemas.VocabularyRead)
async def get_vocabulary_by_id(vocab_id: int, session: SessionDep, current_user: models.User = Depends(manager)) -> models.Vocabulary:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")
        
    vocab = session.get(models.Vocabulary, vocab_id)
    if not vocab:
        raise HTTPException(status_code=404, detail="Vocabulary not found")
    return vocab


@app.post("/associations/", status_code=status.HTTP_201_CREATED, response_model=schemas.AssociationRead)
async def create_association(association: schemas.AssociationCreate, session: SessionDep, current_user: models.User = Depends(manager)) -> models.Association:
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
