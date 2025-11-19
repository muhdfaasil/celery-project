"""
Django settings for celery_project project.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Helper function for environment variables
def env(key, default=None):
    """Get environment variable with optional default value."""
    return os.getenv(key, default)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-change-this-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = [host.strip().rstrip('/') for host in os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')]

# CSRF Configuration
# Parse CSRF trusted origins from environment or use ALLOWED_HOSTS
csrf_origins = env("CSRF_TRUSTED_ORIGINS", default="")
if csrf_origins:
    CSRF_TRUSTED_ORIGINS = [origin.strip().rstrip('/') for origin in csrf_origins.split(',') if origin.strip()]
else:
    # Auto-generate from ALLOWED_HOSTS (add https:// prefix)
    CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS if host not in ['localhost', '127.0.0.1']]
    CSRF_TRUSTED_ORIGINS.extend([f"http://{host}" for host in ALLOWED_HOSTS if host in ['localhost', '127.0.0.1']])

# CSRF Cookie settings for HTTPS
CSRF_COOKIE_SECURE = not DEBUG  # Only secure in production
CSRF_COOKIE_HTTPONLY = False  # Allow JavaScript to read the cookie
CSRF_USE_SESSIONS = False  # Use cookies (default)

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'tasks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'celery_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'celery_project.wsgi.application'

# Database
# --- Database (Azure PostgreSQL Connection String) ---
if os.environ.get("AZURE_POSTGRESQL_CONNECTIONSTRING"):
    CONNECTION = os.environ["AZURE_POSTGRESQL_CONNECTIONSTRING"]
    CONNECTION_STR = {pair.split('=')[0]: pair.split('=')[1] for pair in CONNECTION.split(';') if '=' in pair}
    
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": CONNECTION_STR.get('dbname', ''),
            "HOST": CONNECTION_STR.get('host', ''),
            "USER": CONNECTION_STR.get('user', ''),
            "PASSWORD": CONNECTION_STR.get('password', ''),
            "PORT": CONNECTION_STR.get('Port', '5432'),
            "OPTIONS": {
                "sslmode": "require",
            },
        }
    }
else:
    # Use SQLite for local development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
# Only include static directory if it exists (prevents warnings in Azure)
static_dir = BASE_DIR / 'static'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Celery Configuration
# Handle Azure Redis Cache (SSL) or local Redis
celery_broker = env("CELERY_BROKER_URL", default="redis://localhost:6379/0")
celery_backend = env("CELERY_RESULT_BACKEND", default="redis://localhost:6379/0")

# If Redis URL doesn't start with redis:// or rediss://, add rediss:// for Azure Redis Cache
if not celery_broker.startswith(('redis://', 'rediss://')):
    celery_broker = f"rediss://{celery_broker}"
elif celery_broker.startswith('redis://') and ':6380' in celery_broker:
    # Azure Redis Cache uses SSL on port 6380
    celery_broker = celery_broker.replace('redis://', 'rediss://')

if not celery_backend.startswith(('redis://', 'rediss://')):
    celery_backend = f"rediss://{celery_backend}"
elif celery_backend.startswith('redis://') and ':6380' in celery_backend:
    # Azure Redis Cache uses SSL on port 6380
    celery_backend = celery_backend.replace('redis://', 'rediss://')

CELERY_BROKER_URL = celery_broker
CELERY_RESULT_BACKEND = celery_backend
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

# CORS Configuration
CORS_ALLOWED_ORIGINS = env("CORS_ALLOWED_ORIGINS", default="").split(",") if env("CORS_ALLOWED_ORIGINS") else []
CORS_ALLOWED_ORIGINS = [origin.strip().rstrip('/') for origin in CORS_ALLOWED_ORIGINS if origin.strip()]
CORS_ALLOW_CREDENTIALS = True

