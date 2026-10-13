# How to run the application


## Setup

### virtual environment 
1. Clone the repository `git clone https://github.com/iyanuashiri/chaperone-project.git`
2. cd backend
3. Create a virtual environment `python -m venv venv`
4. Activate the virtual environment `venv\Scripts\activate` or `source venv/bin/activate` on linux
5. Install the requirements `pip install -r requirements.txt`
6. Run the migrations `alembic upgrade head`
7. Run the server `uvicorn app.main:app --reload`

### uv
1. Clone the repository `git clone https://github.com/iyanuashiri/chaperone-project.git`
2. cd backend
3. `uv sync`
4. `uv run alembic upgrade head`
5. `uv run uvicorn app.main:app --reload`

### docker
1. Clone the repository `git clone https://github.com/iyanuashiri/chaperone-project.git`
2. cd backend
3. `docker build -t chaperone-backend .`
4. `docker run --env-file .env -p 8000:8000 chaperone-backend`


## Run migrations
1. `uv run alembic init alembic`
2. `uv run alembic revision --autogenerate -m "message"`
3. `uv run alembic upgrade head`
---

## Architecture

The backend is a **FastAPI + SQLModel + Alembic** app with a clean per-domain layout so each concern (HTTP layer, persistence, and shapes) lives in its own file.

### Directory layout (per domain)

| Domain | models/ | schemas/ | crud/ |
|--------|---------|----------|------|
| Auth + users | models/user.py | schemas/user.py | crud/user.py |
| Vocabulary + associations | models/vocabulary.py | schemas/vocabulary.py | crud/vocabulary.py |
| Restricted URLs | models/url.py | schemas/url.py | crud/url.py |
| Quizzes | models/quiz.py | schemas/quiz.py | crud/quiz.py |
| Adaptive game (speed bump) | models/game.py | schemas/game.py | crud/game.py |

Each models/<domain>.py holds one SQLAlchemy table class (e.g., Vocabulary, Association, GameSession, GameAttempt) with Mapped[...] annotations and SQLModel Relationships. Each schemas/<domain>.py holds the matching Pydantic request/response models. Each crud/<domain>.py holds the session-scoped query functions (create/get/list/delete) so API routes stay thin.

### Adaptive challenge generation

[pp/services/challenge_generator.py](app/services/challenge_generator.py) is the core speed-bump logic (no LLM required):

- **generate_challenge(challenge_type, level)** � returns a self-contained prompt + options with a deterministic, seeded generator.
- **daptive_level(accuracy, current_level)** � raises difficulty when accuracy is high, drops it when low (the paper's adaptive speed-bump intervention).
- **points_for(is_correct, difficulty)** � difficulty-scaled scoring (5 + 2 � difficulty per correct answer).

Game sessions and attempts are persisted via the GameSession/GameAttempt/GameChallenge tables so the extension's math-challenge flow is fully recorded on the backend.
