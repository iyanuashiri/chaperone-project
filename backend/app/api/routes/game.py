from fastapi import APIRouter, Depends, HTTPException

from app.schemas import schemas
from app.api.deps import SessionDep, manager
from app.models import models
from app.crud import (
    create_game_session,
    get_game_session,
    add_attempt,
    increment_challenge_count,
    recent_accuracy,
    current_level,
)
from app.services.challenge_generator import (
    generate_challenge,
    adaptive_level,
    points_for,
)

router = APIRouter(prefix="/game", tags=["Game"])


@router.get("/challenge/", response_model=schemas.ChallengeRead)
async def get_challenge(
    session: SessionDep,
    current_user: models.User = Depends(manager),
    challenge_type: str = "math",
) -> schemas.ChallengeRead:
    """Fetch one adaptive challenge (math or logic)."""
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")

    level = current_level(session, current_user.id)
    accuracy = recent_accuracy(session, current_user.id)
    level = adaptive_level(accuracy, level)

    challenge = generate_challenge(challenge_type=challenge_type, level=level)

    return schemas.ChallengeRead(
        id=f"{challenge['type']}-{challenge['difficulty']}-{challenge['prompt']}",
        type=challenge["type"],
        prompt=challenge["prompt"],
        options=challenge["options"],
        answer=challenge["answer"],
        difficulty=challenge["difficulty"],
    )


@router.post("/session/", response_model=schemas.GameSessionRead)
async def start_session(
    payload: schemas.GameSessionCreate,
    session: SessionDep,
    current_user: models.User = Depends(manager),
) -> schemas.GameSessionRead:
    """Start a new game session (extension or frontend)."""
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")

    return create_game_session(session, current_user.id, payload.source, payload.site_url)


@router.post("/session/{session_id}/answer/", response_model=schemas.GameAnswerResult)
async def submit_answer(
    session_id: int,
    payload: schemas.GameAnswerCreate,
    session: SessionDep,
    current_user: models.User = Depends(manager),
) -> schemas.GameAnswerResult:
    """Record an answer to a challenge within a session."""
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    db_session = get_game_session(session, session_id, current_user.id)
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")

    is_correct = payload.user_answer.strip().lower() == payload.answer.strip().lower()

    add_attempt(session, {
        "session_id": session_id,
        "challenge_type": payload.challenge_type,
        "prompt": payload.prompt,
        "options": ",".join(payload.options),
        "answer": payload.answer,
        "user_answer": payload.user_answer,
        "is_correct": is_correct,
        "difficulty": payload.difficulty,
        "time_taken_s": payload.time_taken_s,
    })
    increment_challenge_count(session, db_session)

    points = points_for(is_correct, payload.difficulty)
    return schemas.GameAnswerResult(
        is_correct=is_correct,
        points_awarded=points,
        correct_answer=payload.answer if not is_correct else None,
    )
