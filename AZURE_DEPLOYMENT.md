# Azure Deployment Guide

This guide covers deploying the Django Celery project to Azure App Service.

## Azure Environment Variables

Based on your Azure configuration, here are the environment variables that need to be set:

### Required Environment Variables

1. **ALLOWED_HOSTS**
   - Value: `https://test-web-app-bfdjhbeycgbuh0g9.centralindia-01.azurewebsites.net/`
   - Note: The trailing slash will be automatically removed by the settings

2. **AZURE_POSTGRESQL_CONNECTIONSTRING**
   - Value: `dbname=postgres;host=celery-test-db.postgres.database.azure.com;user=rohith;password=uthMetro@123`
   - Note: The settings will automatically parse this and add SSL mode

3. **CELERY_BROKER_URL**
   - Value: `redis-celery-test.redis.cache.windows.net:6380/0`
   - Note: The settings will automatically add `rediss://` protocol for SSL

4. **CELERY_RESULT_BACKEND**
   - Value: `redis-celery-test.redis.cache.windows.net:6380/0`
   - Note: The settings will automatically add `rediss://` protocol for SSL

5. **CORS_ALLOWED_ORIGINS**
   - Value: `https://test-web-app-bfdjhbeycgbuh0g9.centralindia-01.azurewebsites.net/`
   - Note: The trailing slash will be automatically removed

6. **DEBUG**
   - Value: `False` (for production)

7. **SECRET_KEY**
   - Value: Your secret key (already set)

8. **SCM_DO_BUILD_DURING_DEPLOYMENT**
   - Value: `1` (enables build during deployment)

## Important Notes

### Azure Redis Cache Authentication

If your Azure Redis Cache requires a password, you need to include it in the connection string:

**Format:** `rediss://:password@host:port/db`

**Example:** `rediss://:your-password@redis-celery-test.redis.cache.windows.net:6380/0`

Update your Azure environment variables:
- `CELERY_BROKER_URL`: `rediss://:your-password@redis-celery-test.redis.cache.windows.net:6380/0`
- `CELERY_RESULT_BACKEND`: `rediss://:your-password@redis-celery-test.redis.cache.windows.net:6380/0`

### Azure PostgreSQL Connection String

The current format is correct. The settings will automatically:
- Parse the connection string
- Extract database credentials
- Add SSL mode requirement

### Static Files

Make sure to run `python manage.py collectstatic` during deployment or add it to your deployment script.

## Deployment Checklist

- [ ] All environment variables are set in Azure App Service
- [ ] Redis password is included in CELERY_BROKER_URL and CELERY_RESULT_BACKEND (if required)
- [ ] Static files are collected (`python manage.py collectstatic`)
- [ ] Database migrations are run (`python manage.py migrate`)
- [ ] Celery worker is configured to run (Azure WebJobs or separate App Service)

## Azure WebJobs for Celery Worker

To run Celery worker on Azure, you can:

1. **Option A: Use Azure WebJobs**
   - Create a WebJob that runs: `celery -A celery_project worker --loglevel=info`

2. **Option B: Use a separate App Service**
   - Deploy a separate App Service instance for the Celery worker
   - Use the same environment variables

3. **Option C: Use Azure Container Instances**
   - Run Celery worker in a container

## Troubleshooting

### Redis Connection Issues

If you get Redis connection errors:
1. Verify the Redis connection string includes password if required
2. Check that port 6380 is open (SSL port)
3. Verify firewall rules allow Azure App Service IPs

### Database Connection Issues

If you get database connection errors:
1. Verify the connection string format
2. Check that SSL is enabled (it's automatically added)
3. Verify firewall rules allow Azure App Service IPs

### CORS Issues

If you get CORS errors:
1. Verify `CORS_ALLOWED_ORIGINS` matches your frontend URL exactly
2. Check that `corsheaders` is in `INSTALLED_APPS`
3. Verify `CorsMiddleware` is in `MIDDLEWARE`

