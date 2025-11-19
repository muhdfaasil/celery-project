# CSRF 403 Error Fix

## Problem
Getting `Forbidden (403) CSRF verification failed` error when submitting forms.

## Solution Applied

### 1. Added CSRF_TRUSTED_ORIGINS
The settings now automatically generate `CSRF_TRUSTED_ORIGINS` from `ALLOWED_HOSTS`:
- For Azure: `https://test-web-app-bfdjhbeycgbuh0g9.centralindia-01.azurewebsites.net`
- For localhost: `http://localhost`, `http://127.0.0.1`

### 2. CSRF Cookie Settings
- `CSRF_COOKIE_SECURE = not DEBUG` - Secure cookies in production (HTTPS)
- `CSRF_COOKIE_HTTPONLY = False` - Allows JavaScript to read the cookie
- `CSRF_USE_SESSIONS = False` - Uses cookies (default)

## How It Works

1. **Automatic Detection**: If `CSRF_TRUSTED_ORIGINS` environment variable is not set, it automatically generates from `ALLOWED_HOSTS`
2. **HTTPS Support**: Automatically adds `https://` prefix for non-localhost hosts
3. **Cookie Settings**: Properly configured for HTTPS in production

## Azure Environment Variables

You can optionally set `CSRF_TRUSTED_ORIGINS` in Azure, but it's not required - it will be auto-generated from `ALLOWED_HOSTS`:

```
CSRF_TRUSTED_ORIGINS=https://test-web-app-bfdjhbeycgbuh0g9.centralindia-01.azurewebsites.net
```

Or leave it unset and it will be generated automatically.

## Verification

After deploying:
1. The CSRF token should be included in forms (via `{% csrf_token %}`)
2. JavaScript can read the cookie (via `getCookie('csrftoken')`)
3. Forms should submit without 403 errors

## If Still Getting 403

1. **Clear browser cookies** for the site
2. **Check browser console** for CSRF token errors
3. **Verify DEBUG=False** in production (CSRF is stricter in production)
4. **Check Azure logs** for specific CSRF error messages

The fix is now in place and should work automatically!

