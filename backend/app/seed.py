"""
Seed the vocabulary table with a starter set of words (word + meaning).

Run:  uv run python -m app.seed
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import engine
from app.models import models

VOCABULARY = [
    # Level 1 - common words
    ("happy", "feeling or showing pleasure"),
    ("big", "of considerable size"),
    ("fast", "moving quickly"),
    ("small", "little in size"),
    ("good", "of high quality"),
    ("bright", "giving out much light"),
    ("quick", "moving fast"),
    ("strong", "having power"),
    ("clean", "free from dirt"),
    ("kind", "friendly and generous"),
    ("brave", "ready to face danger"),
    ("calm", "not nervous or upset"),
    # Level 2 - everyday words
    ("beautiful", "pleasing to look at"),
    ("dangerous", "likely to cause harm"),
    ("difficult", "needing effort or skill"),
    ("important", "of great significance"),
    ("interesting", "holding attention"),
    ("necessary", "needed; essential"),
    ("possible", "able to be done"),
    ("successful", "achieving the desired aim"),
    ("wonderful", "extremely good"),
    ("terrible", "extremely bad"),
    ("famous", "known by many people"),
    ("ancient", "very old"),
    # Level 3 - academic words
    ("analyze", "examine in detail"),
    ("approach", "a way of dealing with something"),
    ("assess", "evaluate or estimate"),
    ("concept", "an abstract idea"),
    ("consistent", "acting alike; steady"),
    ("diverse", "showing great variety"),
    ("efficient", "achieving max productivity"),
    ("evident", "clearly seen or understood"),
    ("fundamental", "forming a necessary base"),
    ("generate", "produce or create"),
    ("hypothesis", "a proposed explanation"),
    ("implement", "put a decision into effect"),
    ("interpret", "explain the meaning of"),
    ("methodology", "a system of methods"),
    ("objective", "not influenced by feelings"),
    ("principle", "a fundamental truth"),
    ("relevant", "closely connected to the matter"),
    ("significant", "sufficiently great to be important"),
    ("strategy", "a plan for achieving a goal"),
    ("theory", "a set of ideas explaining something"),
    ("validate", "check or prove the validity of"),
    ("variable", "an element that can change"),
]


def seed_vocabulary():
    with Session(engine) as session:
        existing = session.scalars(select(models.Vocabulary)).all()
        existing_words = {v.word for v in existing}
        added = 0
        for word, meaning in VOCABULARY:
            if word not in existing_words:
                session.add(models.Vocabulary(word=word, meaning=meaning))
                added += 1
        session.commit()
        print(f"Vocabulary seed: {added} new words added, {len(existing)} already present.")


if __name__ == "__main__":
    seed_vocabulary()
