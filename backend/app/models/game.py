import enum
from datetime import datetime
from typing import List

from sqlalchemy import Integer, String, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, Relationship

from app.models.base import Base


class ChallengeType(enum.Enum):
    MATH = "math"
    LOGIC = "logic"
    VOCABULARY = "vocabulary"


class GameSession(Base):
    __tablename__ = "game_session"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    source: Mapped[str] = mapped_column(String(50), default="extension")  # extension | frontend
    site_url: Mapped[str] = mapped_column(String(500), default="")
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    challenge_count: Mapped[int] = mapped_column(Integer, default=0)

    user: Mapped["User"] = Relationship(back_populates="game_sessions")
    attempts: Mapped[List["GameAttempt"]] = Relationship(back_populates="session", cascade="all, delete-orphan")


class GameAttempt(Base):
    __tablename__ = "game_attempt"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(Integer, ForeignKey("game_session.id"))
    challenge_type: Mapped[ChallengeType] = mapped_column(
        Enum(ChallengeType, name="challenge_type", native_enum=True,
             values_callable=lambda x: [i.value for i in x]),
        default=ChallengeType.MATH.value,
    )
    prompt: Mapped[str] = mapped_column(String(1000))
    options: Mapped[str] = mapped_column(String(2000), default="")  # JSON list of options
    answer: Mapped[str] = mapped_column(String(255))
    user_answer: Mapped[str] = mapped_column(String(255), default="")
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False)
    difficulty: Mapped[int] = mapped_column(Integer, default=1)
    time_taken_s: Mapped[float] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    session: Mapped["GameSession"] = Relationship(back_populates="attempts")
