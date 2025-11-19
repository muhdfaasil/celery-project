import os
import ssl
import logging
from celery import Celery
from dotenv import load_dotenv

# Load environment variables (keeps parity with your settings)
load_dotenv()

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'celery_project.settings')

app = Celery('celery_project')

# Use Django settings with CELERY_ prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# SSL / transport options for Azure Redis (required for rediss://)
# NOTE: Using CERT_NONE is acceptable for quick testing; for production use CERT_REQUIRED with CA bundle.
app.conf.broker_use_ssl = {
    'ssl_cert_reqs': ssl.CERT_NONE
}
# Some backend transports expect options under result_backend_transport_options
app.conf.result_backend_transport_options = {
    'ssl': {'ssl_cert_reqs': ssl.CERT_NONE}
}

# Optional: tuning connection timeouts (helps identify network/firewall issues)
app.conf.broker_transport_options = {
    'socket_timeout': 10,
    'socket_connect_timeout': 10,
}

# Optional logging so you can see connection attempts in App Service logs
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

logger.info("Celery configuration loaded. Broker URL starts with: %s", (os.environ.get('CELERY_BROKER_URL') or "")[:10])

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Simple debug task (you already had this)
@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
