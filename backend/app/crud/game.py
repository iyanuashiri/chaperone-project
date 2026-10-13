from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.game import GameSession, GameAttempt


def create_game_session(session: Session, user_id: int, source: str, site_url: str) -> GameSession:
    db_session = GameSession(user_id=user_id, source=source, site_url=site_url)
    session.add(db_session)
    session.commit()
    session.refresh(db_session)
    return db_session


def get_game_session(session: Session, session_id: int, user_id: int) -> GameSession | None:
    db_session = session.get(GameSession, session_id)
    if db_session and db_session.user_id != user_id:
        return None
    return db_session


def add_attempt(session: Session, attempt_data: dict) -> GameAttempt:
    attempt = GameAttempt(**attempt_data)
    session.add(attempt)
    session.commit()
    session.refresh(attempt)
    return attempt


def increment_challenge_count(session: Session, game_session: GameSession) -> None:
    game_session.challenge_count += 1
    session.commit()


def recent_accuracy(session: Session, user_id: int, limit: int = 10) -> float | None:
    attempts = (
        session.query(GameAttempt)
        .join(GameSession)
        .filter(GameSession.user_id == user_id)
        .order_by(GameAttempt.created_at.desc())
        .limit(limit)
        .all()
    )
    if not attempts:
        return None
    return sum(1 for a in attempts if a.is_correct) / len(attempts)


def current_level(session: Session, user_id: int) -> int:
    last_attempt = (
        session.query(GameAttempt)
        .join(GameSession)
        .filter(GameSession.user_id == user_id)
        .order_by(GameAttempt.created_at.desc())
        .first()
    )
    return last_attempt.difficulty if last_attempt else 1


def list_game_sessions(session: Session, user_id: int) -> list[GameSession]:
    return session.query(GameSession).filter(GameSession.user_id == user_id).all()


def list_attempts(session: Session, session_ids: list[int]) -> list[GameAttempt]:
    if not session_ids:
        return []
    return session.query(GameAttempt).filter(GameAttempt.session_id.in_(session_ids)).all()


def correct_days(session: Session, user_id: int) -> set:
    attempts = (
        session.query(GameAttempt)
        .join(GameSession)
        .filter(GameSession.user_id == user_id, GameAttempt.is_correct == True)  # noqa: E712
        .all()
    )
    return {a.created_at.date() for a in attempts}


def sessions_since(session: Session, user_id: int, since: datetime) -> list[GameSession]:
    return (
        session.query(GameSession)
        .filter(GameSession.user_id == user_id, GameSession.started_at >= since)
        .all()
    )


def attempts_since(session: Session, user_id: int, since: datetime) -> list[GameAttempt]:
    return (
        session.query(GameAttempt)
        .join(GameSession)
        .filter(GameSession.user_id == user_id, GameAttempt.created_at >= since)
        .all()
    )
