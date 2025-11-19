# Azure Startup Command Configuration

## Simplified Startup Command

Since migrations and static files are now handled in GitHub Actions, the startup command is simplified:

### Startup Command for Azure App Service

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
6. Paste: `gunicorn celery_project.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120`
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
   - **Value**: `gunicorn celery_project.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120`
7. Click **OK**
8. Click **Save** at the top
9. Click **Continue** to apply changes

## What Changed

- ✅ **Migrations** - Now run automatically in GitHub Actions after deployment
- ✅ **Static Files** - Now collected automatically in GitHub Actions after deployment
- ✅ **Startup Command** - Only starts Gunicorn server (simpler and faster)

## GitHub Actions Workflow

The workflow now automatically:
1. Deploys your code
2. Runs `python manage.py migrate --noinput`
3. Runs `python manage.py collectstatic --noinput`
4. Restarts the app service

All of this happens during deployment, so the startup command only needs to start the server.

## Adjusting Workers

You can adjust the number of workers based on your App Service plan:

- **Free/Shared**: 1 worker
- **Basic (B1)**: 1-2 workers
- **Standard (S1)**: 2-4 workers
- **Standard (S2/S3)**: 4-8 workers

Example for Basic plan:
```
gunicorn celery_project.wsgi:application --bind 0.0.0.0:8000 --workers 1 --timeout 120
```

## Verification

After setting the startup command:

1. Go to **Log stream** in Azure Portal
2. Restart your App Service
3. You should see Gunicorn startup messages (no migration/collectstatic output)

## Troubleshooting

### If Gunicorn fails to start:
- Check that `gunicorn` is in `requirements.txt` (it is)
- Verify Python version matches (3.12)
- Check application logs for errors
- Verify the startup command is set correctly

### If migrations/static files are missing:
- Check GitHub Actions workflow logs
- Verify the deployment completed successfully
- Check that `AZUREAPPSERVICE_RESOURCEGROUP` secret is set in GitHub
