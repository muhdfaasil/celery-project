# Deployment Updates - Migrations & Static Files in GitHub Actions

## What Changed

Migrations and static files collection are now handled **automatically in GitHub Actions** during deployment, instead of in the startup command. This is better because:

- ✅ **Consistent paths** - No path issues when Azure changes deployment paths
- ✅ **Faster startup** - App starts immediately without running migrations/collectstatic
- ✅ **Better error handling** - See migration/static file errors in GitHub Actions logs
- ✅ **Automatic execution** - Runs on every deployment automatically

## Updated Files

### 1. GitHub Actions Workflow (`.github/workflows/main_test-web-app.yml`)

**Added steps after deployment:**
1. **Get Resource Group** - Automatically detects the resource group
2. **Run Django Migrations** - Executes `python manage.py migrate --noinput`
3. **Collect Static Files** - Executes `python manage.py collectstatic --noinput`
4. **Restart App Service** - Restarts the app to apply changes

### 2. Startup Command (`startup.txt`)

**Simplified to only start Gunicorn:**
```
gunicorn celery_project.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120
```

## Azure Configuration

### Set Startup Command in Azure Portal

1. Go to **Azure Portal** → Your App Service → **Configuration** → **General settings**
2. Set **Startup Command** to:
   ```
   gunicorn celery_project.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120
   ```
3. Click **Save** and **Continue**

**OR** set as environment variable:
- **Name**: `WEBSITE_STARTUP_COMMAND`
- **Value**: `gunicorn celery_project.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120`

## Deployment Flow

When you push to `main` branch:

1. ✅ **GitHub Actions builds** the application
2. ✅ **Deploys** to Azure App Service
3. ✅ **Runs migrations** automatically (via SSH)
4. ✅ **Collects static files** automatically (via SSH)
5. ✅ **Restarts** the app service
6. ✅ **App starts** with Gunicorn (from startup command)

## Benefits

- **No path issues** - Commands run in the correct directory during deployment
- **Faster startup** - App starts immediately, no waiting for migrations
- **Better visibility** - See all deployment steps in GitHub Actions logs
- **Automatic** - No manual intervention needed

## Verification

After deployment, check:

1. **GitHub Actions logs** - Should show:
   - ✅ "Running database migrations..."
   - ✅ "Collecting static files..."
   - ✅ "Application restarted successfully"

2. **Azure Log stream** - Should show:
   - ✅ Gunicorn starting
   - ✅ No migration/collectstatic output (those run during deployment)

## Troubleshooting

### If migrations fail in GitHub Actions:
- Check database connection string in Azure environment variables
- Verify database is accessible
- Check GitHub Actions logs for specific error

### If static files collection fails:
- Verify `STATIC_ROOT` is set in settings.py (it is: `staticfiles/`)
- Check file permissions
- Review GitHub Actions logs

### If app doesn't start:
- Verify startup command is set correctly in Azure
- Check that `gunicorn` is in `requirements.txt` (it is)
- Review Azure Log stream for errors

## No Secrets Required

The workflow automatically detects the resource group from the app service, so you don't need to set `AZUREAPPSERVICE_RESOURCEGROUP` secret in GitHub.

