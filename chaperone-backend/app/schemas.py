from typing import Dict, List
from pydantic import BaseModel, Field
from app.models import AssociationStatus


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    

class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int

    class Config:
        from_attributes = True


class VocabularyCreate(BaseModel):
    word: str
    meaning: str

class VocabularyRead(BaseModel):
    id: int
    word: str
    meaning: str

    class Config:
        from_attributes = True


class OptionBase(BaseModel):
    option: str
    meaning: str
    is_correct: bool


class AssociationCreate(BaseModel):
    vocabulary_id: int


class AssociationRead(BaseModel):
    id: int
    status: AssociationStatus
    user: UserBase
    vocabulary: VocabularyRead
    options: List[OptionBase]

    class Config:
        from_attributes = True


class AssociationSchema(BaseModel):
    vocabulary: str
    options: Dict[str, str] = Field(description="This is a dictionary of options. The key is the option and the value is the meaning.")

