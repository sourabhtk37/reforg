FROM python:3.7

RUN pip install fastapi uvicorn

EXPOSE 80

COPY ./kvstore /app/kvstore
COPY ./logging.conf /app
COPY ./server /app

WORKDIR /app

CMD ["uvicorn", "main:app","--host","0.0.0.0","--port", "80"]


