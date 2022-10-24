# Import the common settings from each template
from .common_settings import *

import environ
import google.auth
import io
import os

from google.cloud import secretmanager
from sys import exit
from urllib.parse import urlparse

env = environ.Env(DEBUG=(bool, True))

# Attempt to load the Project ID into the environment, safely failing on error.
try:
    _, os.environ["GOOGLE_CLOUD_PROJECT"] = google.auth.default()
except google.auth.exceptions.DefaultCredentialsError:
    pass

payload = None
if os.environ.get("CICD", None) or os.environ.get("LOCAL_DEV", None):
    payload = (
        f"DATABASE_URL=sqlite:///{os.path.join(BASE_DIR, 'db.sqlite3')}\n"
        f"SECRET_KEY=mySuperSecretSecretKey!\n"
    )
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
elif os.environ.get("GOOGLE_CLOUD_PROJECT", None):
    # Pull secrets from Secret Manager
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    client = secretmanager.SecretManagerServiceClient()
    settings_name = os.environ.get("SETTINGS_NAME", "django_settings")
    name = f"projects/{project_id}/secrets/{settings_name}/versions/latest"
    payload = client.access_secret_version(
        name=name).payload.data.decode("UTF-8")
else:
    raise Exception(
        "CICD, GOOGLE_CLOUD_PROJECT, or LOCAL_DEV not detected, no secrets found.")

env.read_env(io.StringIO(payload), overwrite=True)

SECRET_KEY = env("SECRET_KEY")

DEBUG = env("DEBUG")

if os.environ.get("CICD", None) or os.environ.get("LOCAL_DEV", None):
    ALLOWED_HOSTS = ["*"]
    CSRF_TRUSTED_ORIGINS = ["https://*..cloudshell.dev",
                            "https://*.cloudworkstations.dev"]
else:
    ALLOWED_HOSTS = [".a.run.app"]
    CSRF_TRUSTED_ORIGINS = ["https://*.a.run.app"]
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")\

ADDITIONAL_HOSTS = env("ADDITIONAL_HOSTS", default="").split(",")
for host in ADDITIONAL_HOSTS:
    clean_host = host.strip()

    if not clean_host:
        continue

    ALLOWED_HOSTS.append(clean_host)
    if clean_host.startswith('.'):
        CSRF_TRUSTED_ORIGINS.append(f"https://*{clean_host}")
    else:
        CSRF_TRUSTED_ORIGINS.append(f"https://{clean_host}")

# Use django-environ to parse the connection string
DATABASES = {"default": env.db()}

# If the flag as been set, configure to use proxy
if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
    DATABASES["default"]["HOST"] = "127.0.0.1"
    DATABASES["default"]["PORT"] = 5432

if env("GS_BUCKET_NAME", default=None):
    # Define static storage via django-storages[google]
    GS_BUCKET_NAME = env("GS_BUCKET_NAME")
    DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    GS_DEFAULT_ACL = "publicRead"
