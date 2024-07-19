# Mini-Hackathon by Kevin Chromik - Challenge 2 "Lecker Lecker"

## Local Setup

### Prerequisites
- Python 3.12 or higher
- poetry
- docker-compose

### Setup Guide
1. Setup new virtual environment
```bash
poetry install
```

2. Start Redis and Postgres via Docker-Compose Setup
```bash
docker-compose up -d redis postgres
```

3. migrate the database
```bash
poetry run python app/manage.py migrate
```

4. Start the Django server
```bash
poetry run python app/manage.py runserver
```
