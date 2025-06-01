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


