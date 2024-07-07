FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libmariadb-dev pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
