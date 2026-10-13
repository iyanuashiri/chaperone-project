from typing import List

from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, Relationship

from app.models.base import Base


class Quiz(Base):
    __tablename__ = "quiz"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str] = mapped_column(String(100000))
    number_of_questions: Mapped[int] = mapped_column(Integer, default=0)
    number_of_options: Mapped[int] = mapped_column(Integer, default=0)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))

    user: Mapped["User"] = Relationship(back_populates="quizzes")
    questions: Mapped[List["Question"]] = Relationship(back_populates="quiz", cascade="all, delete-orphan")


class Question(Base):
    __tablename__ = "question"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quiz_id: Mapped[int] = mapped_column(Integer, ForeignKey("quiz.id"))
    question: Mapped[str] = mapped_column(String(1000))

    quiz: Mapped["Quiz"] = Relationship(back_populates="questions")
    question_options: Mapped[List["QuestionOption"]] = Relationship(back_populates="question", cascade="all, delete-orphan")
    answers: Mapped[List["Answer"]] = Relationship(back_populates="question", cascade="all, delete-orphan")


class QuestionOption(Base):
    __tablename__ = "question_option"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey("question.id"))
    option: Mapped[str] = mapped_column(String(1000))
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False)

    question: Mapped["Question"] = Relationship(back_populates="question_options")
    answers: Mapped[List["Answer"]] = Relationship(back_populates="selected_option", cascade="all, delete-orphan")


class Answer(Base):
    __tablename__ = "answer"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey("question.id"))
    selected_option_id: Mapped[int] = mapped_column(Integer, ForeignKey("question_option.id"))
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False)

    user: Mapped["User"] = Relationship(back_populates="answers")
    question: Mapped["Question"] = Relationship(back_populates="answers")
    selected_option: Mapped["QuestionOption"] = Relationship(back_populates="answers")
