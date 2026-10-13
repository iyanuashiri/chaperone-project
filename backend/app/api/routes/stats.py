from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException

from app.schemas import schemas
from app.api.deps import SessionDep, manager
from app.models import models
from app.crud import (
    list_game_sessions,
    list_attempts,
    correct_days,
    sessions_since,
    attempts_since,
)

router = APIRouter(prefix="/stats", tags=["Stats"])


def _streak_for_user(session, user_id: int) -> int:
    """Number of consecutive days with at least one correct attempt."""
    days = correct_days(session, user_id)
    streak = 0
    day = datetime.now().date()
    while day in days:
        streak += 1
        day -= timedelta(days=1)
    return streak


def points(a: models.GameAttempt) -> int:
    return 5 + a.difficulty * 2


@router.get("/summary", response_model=schemas.StatsSummary)
async def stats_summary(
    session: SessionDep,
    current_user: models.User = Depends(manager),
) -> schemas.StatsSummary:
    """Aggregate stats for the dashboard."""
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")

    game_sessions = list_game_sessions(session, current_user.id)
    session_ids = [s.id for s in game_sessions]
    attempts = list_attempts(session, session_ids)

    total_attempts = len(attempts)
    total_correct = sum(1 for a in attempts if a.is_correct)
    accuracy = (total_correct / total_attempts) if total_attempts else 0.0

    total_points = sum(points(a) for a in attempts if a.is_correct)

    return schemas.StatsSummary(
        total_sessions=len(game_sessions),
        total_attempts=total_attempts,
        total_correct=total_correct,
        accuracy=round(accuracy, 4),
        current_streak=_streak_for_user(session, current_user.id),
        total_points=total_points,
    )


@router.get("/daily", response_model=list[schemas.DailyStat])
async def stats_daily(
    session: SessionDep,
    current_user: models.User = Depends(manager),
    days: int = 30,
) -> list[schemas.DailyStat]:
    """Daily activity for the last N days."""
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")

    since = datetime.now() - timedelta(days=days)

    game_sessions = sessions_since(session, current_user.id, since)
    sessions_by_date: dict = {}
    for gs in game_sessions:
        d = gs.started_at.date()
        sessions_by_date[d] = sessions_by_date.get(d, 0) + 1

    attempts = attempts_since(session, current_user.id, since)
    attempts_by_date: dict = {}
    for a in attempts:
        d = a.created_at.date()
        entry = attempts_by_date.setdefault(d, {"attempts": 0, "correct": 0})
        entry["attempts"] += 1
        entry["correct"] += 1 if a.is_correct else 0

    result: list[schemas.DailyStat] = []
    for i in range(days):
        d = (datetime.now() - timedelta(days=days - 1 - i)).date()
        att = attempts_by_date.get(d, {"attempts": 0, "correct": 0})
        result.append(
            schemas.DailyStat(
                date=d.isoformat(),
                sessions=sessions_by_date.get(d, 0),
                attempts=att["attempts"],
                correct=att["correct"],
                accuracy=round((att["correct"] / att["attempts"]), 4) if att["attempts"] else 0.0,
            )
        )

    return result


@router.get("/sites", response_model=list[schemas.SiteStat])
async def stats_sites(
    session: SessionDep,
    current_user: models.User = Depends(manager),
) -> list[schemas.SiteStat]:
    """Per-site session/attempt breakdown."""
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")

    game_sessions = list_game_sessions(session, current_user.id)
    session_ids = [s.id for s in game_sessions]
    attempts = list_attempts(session, session_ids)

    site_map: dict = {}
    for gs in game_sessions:
        site = gs.site_url or "(unknown)"
        entry = site_map.setdefault(site, {"sessions": 0, "attempts": 0})
        entry["sessions"] += 1

    attempts_by_session: dict = {}
    for a in attempts:
        attempts_by_session[a.session_id] = attempts_by_session.get(a.session_id, 0) + 1
    for gs in game_sessions:
        site = gs.site_url or "(unknown)"
        site_map.setdefault(site, {"sessions": 0, "attempts": 0})
        site_map[site]["attempts"] += attempts_by_session.get(gs.id, 0)

    return [schemas.SiteStat(site_url=site, **counts) for site, counts in site_map.items()]
