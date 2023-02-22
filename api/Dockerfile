FROM python:3.8

WORKDIR /code

COPY ./api/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./api/app /code/app
COPY ./api/.env /code/app/.env
COPY ./pipeline /code/app/pipeline

CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]