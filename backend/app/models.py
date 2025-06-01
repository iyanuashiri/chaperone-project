from typing import List
import enum

from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column, Mapped, Relationship
from sqlalchemy import Enum 
from sqlalchemy import ForeignKey

from app.core.security import generate_hashed_password


class Base(DeclarativeBase):
    pass


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
   
    def set_password(self, raw_password):
        self.password = generate_hashed_password(raw_password=raw_password)


class Vocabulary(Base):
    __tablename__ = "vocabulary"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    word: Mapped[str] = mapped_column(String(50))
    meaning: Mapped[str] = mapped_column(String(50))

    associations: Mapped[List["Association"]] = Relationship(back_populates="vocabulary", cascade="all, delete-orphan")


class AssociationStatus(enum.Enum):
    PENDING = "pending"
    CORRECT = "correct"
    INCORRECT = "incorrect"


class Association(Base):
    __tablename__ = "association"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status: Mapped[AssociationStatus] = mapped_column(Enum(AssociationStatus, name="association_status", native_enum=True, values_callable=lambda x: [i.value for i in x]), default=AssociationStatus.PENDING.value)
    number_of_times_played: Mapped[int] = mapped_column(Integer, default=0)
    number_of_times_correct: Mapped[int] = mapped_column(Integer, default=0)
    number_of_times_incorrect: Mapped[int] = mapped_column(Integer, default=0)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    user: Mapped["User"] = Relationship(back_populates="associations")

    vocabulary_id: Mapped[int] = mapped_column(Integer, ForeignKey("vocabulary.id"))
    vocabulary: Mapped["Vocabulary"] = Relationship(back_populates="associations")

    options: Mapped[List["Option"]] = Relationship(back_populates="association", cascade="all, delete-orphan")

    def correct_option(self):
        self.status = AssociationStatus.CORRECT
        self.number_of_times_played += 1
        self.number_of_times_correct += 1

    def incorrect_option(self):
        self.status = AssociationStatus.INCORRECT
        self.number_of_times_played += 1
        self.number_of_times_incorrect += 1


class Option(Base):
    __tablename__ = "option"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    option: Mapped[str] = mapped_column(String(255))
    meaning: Mapped[str] = mapped_column(String(255))
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False)

    association_id: Mapped[int] = mapped_column(Integer, ForeignKey("association.id"))
    association: Mapped["Association"] = Relationship(back_populates="options")