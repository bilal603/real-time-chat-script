FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app

RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["sh","-c","daphne -b 0.0.0.0 -p $PORT config.asgi:application"]
