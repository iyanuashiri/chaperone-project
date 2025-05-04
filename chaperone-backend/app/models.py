from sqlmodel import Field, SQLModel, Relationship 
from pydantic import EmailStr, HttpUrl

from app.core.security import generate_hashed_password


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: EmailStr = Field(max_length=255, index=True, unique=True)
    password: str  
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)

    associations: list["Association"] = Relationship(back_populates="user")
    
    def set_password(self, raw_password):
        self.password = generate_hashed_password(raw_password=raw_password)
        self.save()


class Vocabulary(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)  
    word: str    
    meaning: str    

    associations: list["Association"] = Relationship(back_populates="vocabulary")


class Association(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="associations")

    vocabulary_id: int = Field(foreign_key="vocabulary.id")
    vocabulary: "Vocabulary" = Relationship(back_populates="associations")
    
    options: list["Option"] = Relationship(back_populates="association")


class Option(SQLModel, table=True):    
    id: int | None = Field(default=None, primary_key=True)
    option: str = Field(max_length=255)
    meaning: str = Field(max_length=255)
    is_correct: bool = Field(default=False)

    association_id: int = Field(foreign_key="association.id")
    association: "Association" = Relationship(back_populates="options")
