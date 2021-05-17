FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY ./kvstore /app/kvstore
COPY ./logging.conf /app
COPY ./server /app