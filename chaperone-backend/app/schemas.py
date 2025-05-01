from typing import Dict
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    

class AssociationSchema(BaseModel):
    vocabulary: str
    options: Dict[str, str] = Field(description="This is a dictionary of options. The key is the option and the value is the meaning.")


class VocabularyCreate(BaseModel):
    word: str
    meaning: str

class VocabularyRead(BaseModel):
    id: int
    word: str
    meaning: str

    class Config:
        from_attributes = True