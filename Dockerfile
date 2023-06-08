FROM tiangolo/uvicorn-gunicorn-fastapi

COPY ./backend/ /app

COPY ./.env-fordocker /app/.env

RUN pip install -r /app/requirements.txt

