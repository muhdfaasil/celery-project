# Azure Startup Command Configuration

## Startup Command for Azure App Service

Copy and paste this command into Azure Portal:

### Option 1: Full Command (Recommended)
```
python manage.py migrate --noinput; python manage.py collectstatic --noinput; gunicorn celery_project.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120
```

### Option 2: With Error Handling
```
python manage.py migrate --noinput || exit 1; python manage.py collectstatic --noinput || exit 1; gunicorn celery_project.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120
```

### Option 3: Minimal (if migrations/static already handled)
```
gunicorn celery_project.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120
```

## How to Set in Azure Portal

### Method 1: Configuration > General Settings (Recommended)

1. Go to **Azure Portal**
2. Navigate to your App Service: **test-web-app**
3. Go to **Configuration** in the left menu
4. Click on **General settings** tab
5. Scroll down to **Startup Command**
6. Paste the startup command from Option 1 above
7. Click **Save** at the top
8. Click **Continue** to apply changes

### Method 2: Environment Variables

1. Go to **Azure Portal**
2. Navigate to your App Service: **test-web-app**
3. Go to **Configuration** in the left menu
4. Click on **Application settings** tab
5. Click **+ New application setting**
6. Set:
   - **Name**: `WEBSITE_STARTUP_COMMAND`
   - **Value**: `python manage.py migrate --noinput; python manage.py collectstatic --noinput; gunicorn celery_project.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120`
7. Click **OK**
8. Click **Save** at the top
9. Click **Continue** to apply changes

## Command Breakdown

- `python manage.py migrate --noinput` - Runs database migrations automatically
- `python manage.py collectstatic --noinput` - Collects static files for production
- `gunicorn celery_project.wsgi:application` - Starts the Gunicorn WSGI server
- `--bind 0.0.0.0:8000` - Binds to all interfaces on port 8000 (Azure's default)
- `--workers 2` - Uses 2 worker processes (adjust based on your needs)
- `--timeout 120` - Sets timeout to 120 seconds (for long-running requests)

## Adjusting Workers

You can adjust the number of workers based on your App Service plan:

- **Free/Shared**: 1 worker
- **Basic (B1)**: 1-2 workers
- **Standard (S1)**: 2-4 workers
- **Standard (S2/S3)**: 4-8 workers

Example for Basic plan:
```
python manage.py migrate --noinput; python manage.py collectstatic --noinput; gunicorn celery_project.wsgi:application --bind 0.0.0.0:8000 --workers 1 --timeout 120
```

## Verification

After setting the startup command:

1. Go to **Log stream** in Azure Portal
2. Restart your App Service
3. You should see:
   - Migration output
   - Static files collection output
   - Gunicorn startup messages

## Troubleshooting

### If migrations fail:
- Check database connection string
- Verify database is accessible from Azure
- Check logs in **Log stream**

### If static files fail:
- Verify `STATIC_ROOT` is set in settings.py (it is: `staticfiles/`)
- Check file permissions
- Static files should be collected during deployment

### If Gunicorn fails to start:
- Check that `gunicorn` is in `requirements.txt` (it is)
- Verify Python version matches (3.12)
- Check application logs for errors

## Alternative: Using startup.sh

If you prefer using the bash script:

1. Set startup command to: `bash startup.sh`
2. Make sure `startup.sh` is in your repository root
3. The script will handle migrations and static files

