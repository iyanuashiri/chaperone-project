from datetime import datetime

from pydantic import BaseModel


class URLCreate(BaseModel):
    url: str


class URLRead(BaseModel):
    id: int
    url: str
    title: str
    description: str
    date_added: datetime
