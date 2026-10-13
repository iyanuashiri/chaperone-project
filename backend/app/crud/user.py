from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate


def get_user_by_email(session: Session, email: str) -> User | None:
    return session.query(User).filter(User.email == email).first()


def get_user_by_id(session: Session, user_id: int) -> User | None:
    return session.get(User, user_id)


def create_user(session: Session, payload: UserCreate) -> User:
    db_user = User(
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
    )
    db_user.set_password(payload.password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def list_users(session: Session) -> list[User]:
    return session.query(User).all()
