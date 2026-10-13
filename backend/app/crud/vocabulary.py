from sqlalchemy.orm import Session

from app.models.vocabulary import Vocabulary, Association, Option
from app.schemas.vocabulary import VocabularyCreate


def get_vocabulary(session: Session, vocabulary_id: int) -> Vocabulary | None:
    return session.get(Vocabulary, vocabulary_id)


def get_vocabulary_by_word(session: Session, word: str) -> Vocabulary | None:
    return session.query(Vocabulary).filter(Vocabulary.word == word).first()


def list_vocabularies(session: Session) -> list[Vocabulary]:
    return session.query(Vocabulary).all()


def create_vocabulary(session: Session, payload: VocabularyCreate) -> Vocabulary:
    db_vocab = Vocabulary(word=payload.word, meaning=payload.meaning)
    session.add(db_vocab)
    session.commit()
    session.refresh(db_vocab)
    return db_vocab


def get_association(session: Session, association_id: int, user_id: int) -> Association | None:
    return session.query(Association).filter(
        Association.id == association_id,
        Association.user_id == user_id,
    ).first()


def list_associations(session: Session, user_id: int) -> list[Association]:
    return (
        session.query(Association)
        .order_by(Association.id.desc())
        .filter(Association.user_id == user_id)
        .all()
    )


def create_association(session: Session, user_id: int, vocabulary_id: int) -> Association:
    db_association = Association(user_id=user_id, vocabulary_id=vocabulary_id)
    session.add(db_association)
    session.commit()
    session.refresh(db_association)
    return db_association


def create_option(session: Session, association_id: int, option: str, meaning: str, is_correct: bool) -> Option:
    db_option = Option(
        option=option,
        meaning=meaning,
        is_correct=is_correct,
        association_id=association_id,
    )
    session.add(db_option)
    session.commit()
    session.refresh(db_option)
    return db_option
