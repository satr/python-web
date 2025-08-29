FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src .

EXPOSE 8001
USER 1000
CMD ["gunicorn", "app:create_app()", "-w", "4", "-b", "0.0.0.0:8001", "--log-level", "info"]
