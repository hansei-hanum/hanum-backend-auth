FROM python:latest

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["/run.sh"]

EXPOSE 80 50051