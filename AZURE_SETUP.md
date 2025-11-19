# Azure App Service Setup Guide

This guide explains how to configure your Django Celery project on Azure App Service.

## Prerequisites

- Azure App Service created and configured
- Azure PostgreSQL database (or connection string)
- Azure Redis Cache (or connection string)
- All environment variables set in Azure Portal

## Azure Configuration Steps

### 1. Set Environment Variables in Azure Portal

Go to **Azure Portal > Your App Service > Configuration > Application settings** and add:

```
ALLOWED_HOSTS=https://test-web-app-bfdjhbeycgbuh0g9.centralindia-01.azurewebsites.net
AZURE_POSTGRESQL_CONNECTIONSTRING=dbname=postgres;host=celery-test-db.postgres.database.azure.com;user=rohith;password=uthMetro@123
CELERY_BROKER_URL=redis-celery-test.redis.cache.windows.net:6380/0
CELERY_RESULT_BACKEND=redis-celery-test.redis.cache.windows.net:6380/0
CORS_ALLOWED_ORIGINS=https://test-web-app-bfdjhbeycgbuh0g9.centralindia-01.azurewebsites.net
DEBUG=False
SECRET_KEY=$1bq%5)$we-vg_2r%3eq_s_)!dfsw@jwjujh22y%n_coht50!d
SCM_DO_BUILD_DURING_DEPLOYMENT=1
```

**Important Notes:**
- Remove trailing slashes from URLs (the settings file handles this automatically)
- If Redis requires a password, use format: `rediss://:password@host:port/db`
- The settings file will automatically add `rediss://` protocol for Azure Redis Cache

### 2. Configure Startup Command

Go to **Azure Portal > Your App Service > Configuration > General settings** and set:

**Startup Command:**
```
python manage.py migrate --noinput; python manage.py collectstatic --noinput; gunicorn celery_project.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120
```

**OR** set as environment variable:
```
WEBSITE_STARTUP_COMMAND=python manage.py migrate --noinput; python manage.py collectstatic --noinput; gunicorn celery_project.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120
```

### 3. Verify Settings File Usage

The `settings.py` file automatically:
- ✅ Loads environment variables from Azure (via `os.getenv()`)
- ✅ Parses Azure PostgreSQL connection string
- ✅ Handles Azure Redis Cache with SSL (port 6380)
- ✅ Configures CORS from environment variables
- ✅ Strips trailing slashes from URLs
- ✅ Uses SQLite locally if Azure connection string is not set

### 4. GitHub Actions Workflow

The GitHub Actions workflow (`.github/workflows/main_test-web-app.yml`) will:
- Build the application
- Deploy to Azure App Service
- Oryx will automatically install dependencies (via `SCM_DO_BUILD_DURING_DEPLOYMENT=1`)

### 5. Post-Deployment Steps

After deployment, the startup command will automatically:
1. Run database migrations (`python manage.py migrate --noinput`)
2. Collect static files (`python manage.py collectstatic --noinput`)
3. Start Gunicorn server

### 6. Setting Up Celery Worker

You need to run Celery worker separately. Options:

#### Option A: Azure WebJobs
1. Create a WebJob in Azure Portal
2. Upload a script that runs: `celery -A celery_project worker --loglevel=info`
3. Set it to run continuously

#### Option B: Separate App Service
1. Create a separate App Service for Celery worker
2. Use the same environment variables
3. Set startup command: `celery -A celery_project worker --loglevel=info`

#### Option C: Azure Container Instances
1. Deploy Celery worker as a container
2. Use the same environment variables

## Troubleshooting

### Settings File Not Loading Environment Variables

The settings file uses `os.getenv()` which automatically reads from Azure App Service environment variables. No `.env` file is needed in Azure.

### Redis Connection Issues

If you get Redis connection errors:
1. Check if password is required and included in connection string
2. Verify port 6380 is used (SSL port for Azure Redis Cache)
3. The settings file automatically converts to `rediss://` for SSL

### Database Connection Issues

The settings file automatically:
- Parses the Azure PostgreSQL connection string
- Adds SSL mode requirement
- Extracts all connection parameters

### Static Files Not Loading

Make sure:
1. `STATIC_ROOT` is set (it's set to `staticfiles/`)
2. Startup command includes `collectstatic`
3. Azure App Service is configured to serve static files

### CORS Issues

Verify:
1. `CORS_ALLOWED_ORIGINS` matches your frontend URL exactly
2. `corsheaders` is in `INSTALLED_APPS` (it is)
3. `CorsMiddleware` is in `MIDDLEWARE` (it is, positioned early)

## Testing Locally with Azure Settings

To test locally with Azure-like settings, create a `.env` file with:

```env
ALLOWED_HOSTS=localhost,127.0.0.1
AZURE_POSTGRESQL_CONNECTIONSTRING=dbname=postgres;host=your-azure-db.postgres.database.azure.com;user=user;password=pass
CELERY_BROKER_URL=rediss://:password@your-redis.redis.cache.windows.net:6380/0
CELERY_RESULT_BACKEND=rediss://:password@your-redis.redis.cache.windows.net:6380/0
DEBUG=True
SECRET_KEY=your-secret-key
```

The settings file will work the same way in both local and Azure environments!

