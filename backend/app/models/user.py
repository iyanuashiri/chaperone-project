from typing import List

from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import mapped_column, Mapped, Relationship

from app.core.security import generate_hashed_password
from app.models.base import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)

    associations: Mapped[List["Association"]] = Relationship(back_populates="user", cascade="all, delete-orphan")
    urls: Mapped[List["URL"]] = Relationship(back_populates="user", cascade="all, delete-orphan")
    quizzes: Mapped[List["Quiz"]] = Relationship(back_populates="user", cascade="all, delete-orphan")
    answers: Mapped[List["Answer"]] = Relationship(back_populates="user", cascade="all, delete-orphan")
    game_sessions: Mapped[List["GameSession"]] = Relationship(back_populates="user", cascade="all, delete-orphan")

    def set_password(self, raw_password):
        self.password = generate_hashed_password(raw_password=raw_password)
