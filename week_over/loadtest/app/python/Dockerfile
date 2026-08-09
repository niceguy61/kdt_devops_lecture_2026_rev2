FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements-observability.txt ./
RUN pip install --no-cache-dir "setuptools==70.3.0" -r requirements.txt -r requirements-observability.txt

COPY main.py ./

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
