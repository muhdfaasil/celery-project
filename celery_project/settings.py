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
def parse_redis_connection(connection_string):
    """
    Parse Redis connection string in various formats:
    1. StackExchange.Redis format: host:port,password=xxx,ssl=True
    2. Redis URL format: redis://host:port/db or rediss://:password@host:port/db
    3. Simple format: host:port/db
    Returns a properly formatted Redis URL for Celery.
    """
    if not connection_string:
        return "redis://localhost:6379/0"
    
    # If already a Redis URL, return as is
    if connection_string.startswith(('redis://', 'rediss://')):
        return connection_string
    
    # Parse StackExchange.Redis connection string format
    # Format: host:port,password=xxx,ssl=True,abortConnect=False
    if ',' in connection_string:
        params = {}
        parts = connection_string.split(',')
        host_port = parts[0]
        
        # Parse key-value pairs
        for part in parts[1:]:
            if '=' in part:
                key, value = part.split('=', 1)
                params[key.strip().lower()] = value.strip()
        
        # Extract host and port
        if ':' in host_port:
            host, port = host_port.rsplit(':', 1)
        else:
            host = host_port
            port = '6379'
        
        # Build Redis URL
        scheme = 'rediss' if params.get('ssl', '').lower() == 'true' else 'redis'
        password = params.get('password', '')
        db = params.get('db', '0')
        
        if password:
            return f"{scheme}://:{password}@{host}:{port}/{db}"
        else:
            return f"{scheme}://{host}:{port}/{db}"
    
    # Simple format: host:port/db or host:port
    if '/' in connection_string:
        host_port, db = connection_string.rsplit('/', 1)
    else:
        host_port = connection_string
        db = '0'
    
    if ':' in host_port:
        host, port = host_port.rsplit(':', 1)
    else:
        host = host_port
        port = '6379'
    
    # Azure Redis Cache uses SSL on port 6380
    scheme = 'rediss' if port == '6380' else 'redis'
    return f"{scheme}://{host}:{port}/{db}"

celery_broker = env("CELERY_BROKER_URL", default="redis://localhost:6379/0")
celery_backend = env("CELERY_RESULT_BACKEND", default="redis://localhost:6379/0")

# Parse and format Redis connections
celery_broker = parse_redis_connection(celery_broker)
celery_backend = parse_redis_connection(celery_backend)

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

