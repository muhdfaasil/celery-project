# Django Celery Project

A simple Django project with Celery, PostgreSQL, and Redis integration. This project demonstrates how to set up and use Celery for asynchronous task processing.

## Features

- ✅ Django 4.2.7
- ✅ Celery 5.3.4 for asynchronous task processing
- ✅ PostgreSQL database
- ✅ Redis as message broker and result backend
- ✅ Simple web interface to trigger and monitor tasks
- ✅ Environment variable configuration with `.env` file

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- PostgreSQL (running and accessible)
- Redis (running and accessible)
- `python3-venv` package (for creating virtual environment)

### Install Prerequisites (Ubuntu/Debian)

```bash
# Install Python venv
sudo apt install python3-venv

# Install PostgreSQL (if not already installed)
sudo apt install postgresql postgresql-contrib

# Install Redis (if not already installed)
sudo apt install redis-server
```

## Project Structure

```
celery-project/
├── celery_project/          # Main Django project
│   ├── __init__.py
│   ├── celery.py            # Celery configuration
│   ├── settings.py          # Django settings
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   └── manage.py
├── tasks/                   # Django app with Celery tasks
│   ├── __init__.py
│   ├── apps.py
│   ├── tasks.py            # Celery task definitions
│   ├── views.py            # Django views
│   └── urls.py
├── templates/              # HTML templates
│   └── tasks/
│       └── index.html
├── static/                 # Static files
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create from .env.example)
├── .env.example            # Example environment file
└── README.md
```

## Setup Instructions

### 1. Create Virtual Environment

```bash
cd /home/fazil/celery-project
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Database

The project supports two database configurations:

#### Option A: Azure PostgreSQL (Production)

If you have an Azure PostgreSQL connection string, set it as an environment variable:

```bash
export AZURE_POSTGRESQL_CONNECTIONSTRING="host=your-server.postgres.database.azure.com;port=5432;dbname=your-db;user=your-user@your-server;password=your-password;sslmode=require"
```

Or add it to your `.env` file:
```env
AZURE_POSTGRESQL_CONNECTIONSTRING=host=your-server.postgres.database.azure.com;port=5432;dbname=your-db;user=your-user@your-server;password=your-password;sslmode=require
```

#### Option B: SQLite (Local Development - Default)

If `AZURE_POSTGRESQL_CONNECTIONSTRING` is not set, the project will automatically use SQLite for local development. No additional setup is required - the database file (`db.sqlite3`) will be created automatically when you run migrations.

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Create .env file
cat > .env << EOF
# Django Settings
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Azure PostgreSQL (Optional - if not set, SQLite will be used)
# AZURE_POSTGRESQL_CONNECTIONSTRING=host=your-server.postgres.database.azure.com;port=5432;dbname=your-db;user=your-user@your-server;password=your-password;sslmode=require

# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
EOF
```

### 5. Start Redis Server

```bash
# Start Redis (if not running)
sudo systemctl start redis-server

# Verify Redis is running
redis-cli ping
# Should return: PONG
```

### 6. Run Database Migrations

```bash
python manage.py migrate
```

**Note:** If using SQLite (local development), the `db.sqlite3` file will be created automatically. If using Azure PostgreSQL, make sure your connection string is set correctly.

### 7. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

## Running the Application

### Terminal 1: Start Django Development Server

```bash
source venv/bin/activate
python manage.py runserver
```

The Django server will be available at `http://127.0.0.1:8000/`

### Terminal 2: Start Celery Worker

```bash
source venv/bin/activate
celery -A celery_project worker --loglevel=info
```

### Terminal 3: Start Celery Beat (Optional - for periodic tasks)

```bash
source venv/bin/activate
celery -A celery_project beat --loglevel=info
```

## Usage

1. Open your browser and navigate to `http://127.0.0.1:8000/`
2. You'll see a web interface with three task types:
   - **Add Numbers Task**: Adds two numbers (simulates 5-second delay)
   - **Send Email Task**: Simulates sending an email (3-second delay)
   - **Process Data Task**: Processes data (2-second delay)
3. Fill in the forms and click the buttons to trigger tasks
4. Watch the Celery worker terminal to see task execution logs

## Available Tasks

### 1. `add_numbers(x, y)`
Adds two numbers with a 5-second delay.

### 2. `send_email_task(email, subject, message)`
Simulates sending an email with a 3-second delay.

### 3. `process_data_task(data)`
Processes data with a 2-second delay.

## API Endpoints

- `GET /` - Main page with task interface
- `POST /api/add-task/` - Trigger add numbers task
- `POST /api/email-task/` - Trigger email task
- `POST /api/process-task/` - Trigger process data task

## Monitoring Tasks

You can monitor Celery tasks using:

1. **Celery Flower** (optional):
   ```bash
   pip install flower
   celery -A celery_project flower
   ```
   Then visit `http://localhost:5555`

2. **Redis CLI**:
   ```bash
   redis-cli
   KEYS *
   ```

## Troubleshooting

### Database Connection Issues

**For Azure PostgreSQL:**
- Verify `AZURE_POSTGRESQL_CONNECTIONSTRING` environment variable is set correctly
- Check connection string format: `host=...;port=...;dbname=...;user=...;password=...;sslmode=require`
- Ensure SSL is enabled (sslmode=require)
- Verify firewall rules allow your IP address

**For SQLite (Local):**
- SQLite is used automatically if `AZURE_POSTGRESQL_CONNECTIONSTRING` is not set
- The `db.sqlite3` file will be created in the project root
- Ensure the project directory has write permissions

### Redis Connection Issues
- Ensure Redis is running: `sudo systemctl status redis-server`
- Test Redis connection: `redis-cli ping`
- Check Redis configuration in `.env` file

### Celery Worker Not Starting
- Ensure Redis is running
- Check Celery configuration in `celery_project/celery.py`
- Verify broker URL in `settings.py`

### Import Errors
- Ensure virtual environment is activated
- Verify all dependencies are installed: `pip list`
- Check Python path and Django settings

## Development

### Adding New Tasks

1. Add task function to `tasks/tasks.py`:
   ```python
   from celery import shared_task
   
   @shared_task
   def my_new_task(param1, param2):
       # Your task logic here
       return result
   ```

2. Create view in `tasks/views.py` to trigger the task
3. Add URL route in `tasks/urls.py`
4. Update frontend template if needed

## Production Considerations

- Change `SECRET_KEY` in `.env`
- Set `DEBUG=False`
- Configure proper `ALLOWED_HOSTS`
- Use environment-specific database credentials
- Set up proper logging
- Use a process manager (supervisor, systemd) for Celery workers
- Configure Redis persistence
- Set up database backups

## License

This project is open source and available for educational purposes.
