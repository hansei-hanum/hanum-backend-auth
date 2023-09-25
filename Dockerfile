FROM python:latest

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "main:app", "--workers", "8", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:80"]

EXPOSE 80