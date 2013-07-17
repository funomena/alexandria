from alexandria.settings.base import *

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

EMAIL_HOST = os.environ.get("EMAIL_HOST", "localhost")
EMAIL_PORT = os.environ.get("EMAIL_PORT", "1025")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "alexandria")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "alexandria")

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG=False