# Quick Start Guide

## 1. Create Virtual Environment

```bash
cd /home/fazil/celery-project
python3 -m venv venv
source venv/bin/activate
```

If you get an error about `python3-venv`, install it:
```bash
sudo apt install python3-venv
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Configure Database

**Option A: Azure PostgreSQL (Production)**
Set the connection string as an environment variable:
```bash
export AZURE_POSTGRESQL_CONNECTIONSTRING="host=your-server.postgres.database.azure.com;port=5432;dbname=your-db;user=your-user@your-server;password=your-password;sslmode=require"
```

**Option B: SQLite (Local Development - Default)**
If `AZURE_POSTGRESQL_CONNECTIONSTRING` is not set, SQLite will be used automatically. No setup needed!

## 4. Create .env File

Create a `.env` file in the project root:

```env
SECRET_KEY=django-insecure-change-this-in-production-12345
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Azure PostgreSQL (Optional - if not set, SQLite will be used)
# AZURE_POSTGRESQL_CONNECTIONSTRING=host=your-server.postgres.database.azure.com;port=5432;dbname=your-db;user=your-user@your-server;password=your-password;sslmode=require

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

## 5. Start Services

### Start Redis:
```bash
sudo systemctl start redis-server
redis-cli ping  # Should return PONG
```

## 6. Run Migrations

```bash
python manage.py migrate
```

## 7. Run the Application

### Terminal 1 - Django Server:
```bash
source venv/bin/activate
python manage.py runserver
```

### Terminal 2 - Celery Worker:
```bash
source venv/bin/activate
celery -A celery_project worker --loglevel=info
```

## 8. Access the Application

Open your browser and go to: `http://127.0.0.1:8000/`

You should see the Celery Task Manager interface where you can trigger tasks!

