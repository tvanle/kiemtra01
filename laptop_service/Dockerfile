FROM python:3.10-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
WORKDIR /app/catalog
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["sh", "-c", "sleep 10 && python manage.py makemigrations laptop_app && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
