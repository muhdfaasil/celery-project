# Django Admin UI Missing Styles - Static Files Fix

## Problem
Django admin interface appears unstyled (plain HTML without CSS/JS) because static files aren't being served.

## Solution

### 1. Updated URLs to Serve Static Files
Added static file serving in `celery_project/urls.py` - this will serve files from `STATIC_ROOT`.

### 2. Run collectstatic in Azure

You need to run `collectstatic` to gather all static files (including Django admin CSS/JS) into the `staticfiles/` directory.

**In Azure SSH, run:**
```bash
cd /home/site/wwwroot
python manage.py collectstatic --noinput
```

This will:
- Collect all static files from Django apps (including admin)
- Put them in `/home/site/wwwroot/staticfiles/`
- Make them available at `/static/` URL

### 3. Update Startup Command (Optional)

If you want static files collected automatically on each deployment, update your Azure startup command to:

```
python manage.py collectstatic --noinput; gunicorn celery_project.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120
```

**OR** add it to your GitHub Actions workflow after deployment.

## Verification

After running `collectstatic`:
1. Check that `staticfiles/` directory exists in `/home/site/wwwroot/`
2. Check that `staticfiles/admin/` contains CSS and JS files
3. Refresh the admin page - it should now be styled

## Why This Happened

- `collectstatic` wasn't run, so Django admin CSS/JS files weren't collected
- Static files need to be in `STATIC_ROOT` (staticfiles/) to be served
- The URLs now include static file serving, but files need to exist first

## Quick Fix

Run this in Azure SSH:
```bash
cd /home/site/wwwroot
python manage.py collectstatic --noinput
```

Then restart your app or refresh the admin page!

