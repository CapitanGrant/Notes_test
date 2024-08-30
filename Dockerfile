FROM python:3.10-slim

WORKDIR /app

# Установка PostgreSQL
RUN apt-get update && apt-get install -y postgresql-client
RUN apt-get update && apt-get install -y libpq-dev

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

