from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class ChallengeRead(BaseModel):
    """A single adaptive challenge served to the extension or frontend."""
    id: str
    type: str  # math | logic | vocabulary
    prompt: str
    options: List[str] = Field(default_factory=list)  # for choice-based challenges
    answer: str = ""  # correct answer; lets the client evaluate the speed bump
    difficulty: int = 1
    session_id: int | None = None


class GameSessionCreate(BaseModel):
    """Start a new game session."""
    source: str = "extension"  # extension | frontend
    site_url: str = ""


class GameSessionRead(BaseModel):
    id: int
    source: str
    site_url: str
    started_at: datetime
    ended_at: datetime | None = None
    challenge_count: int

    class Config:
        from_attributes = True


class GameAnswerCreate(BaseModel):
    """Record an answer to a challenge."""
    challenge_type: str = "math"  # math | logic | vocabulary
    prompt: str
    options: List[str] = Field(default_factory=list)
    answer: str
    user_answer: str
    difficulty: int = 1
    time_taken_s: float = 0


class GameAnswerResult(BaseModel):
    is_correct: bool
    points_awarded: int
    correct_answer: str | None = None


class StatsSummary(BaseModel):
    total_sessions: int
    total_attempts: int
    total_correct: int
    accuracy: float = 0.0
    current_streak: int = 0
    total_points: int = 0


class DailyStat(BaseModel):
    date: str
    sessions: int = 0
    attempts: int = 0
    correct: int = 0
    accuracy: float = 0.0


class SiteStat(BaseModel):
    site_url: str
    sessions: int = 0
    attempts: int = 0
