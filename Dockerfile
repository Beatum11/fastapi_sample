FROM python:3.11-slim

# setting environment
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

COPY . .

# starting
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]