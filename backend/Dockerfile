FROM python:3.12-bookworm

LABEL version="1.0.0"

WORKDIR /code


COPY requirements.txt /code/requirements.txt

RUN python3 -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r /code/requirements.txt

COPY app /code/app 
COPY alembic /code/alembic
COPY alembic.ini /code/alembic.ini

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 

CMD ["venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "78"]