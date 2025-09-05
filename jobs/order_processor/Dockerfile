FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src .

USER 1000
EXPOSE 8002
CMD ["python", "main.py"]
