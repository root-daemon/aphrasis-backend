FROM python:3.12.8-slim

# Set Python to run in unbuffered mode
ENV PYTHONUNBUFFERED=1
# Disable Python's byte code generation
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
        libsndfile1 \
        libsndfile1-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH="/app:/app/app:${PYTHONPATH}"

RUN ln -s /app/app/models /app/models

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 