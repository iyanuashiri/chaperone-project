from sqlalchemy.orm import Session

from app.models.url import URL
from app.schemas.url import URLCreate


def get_url(session: Session, url_id: int, user_id: int) -> URL | None:
    return session.query(URL).filter(URL.id == url_id, URL.user_id == user_id).first()


def list_urls(session: Session, user_id: int) -> list[URL]:
    return session.query(URL).filter(URL.user_id == user_id).all()


def create_url(session: Session, user_id: int, payload: URLCreate, title: str, description: str) -> URL:
    db_url = URL(
        url=payload.url,
        title=title,
        description=description,
        user_id=user_id,
    )
    session.add(db_url)
    session.commit()
    session.refresh(db_url)
    return db_url


def delete_url(session: Session, url: URL) -> None:
    session.delete(url)
    session.commit()
