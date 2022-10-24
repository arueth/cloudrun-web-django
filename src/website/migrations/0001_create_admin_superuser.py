import os

from django.contrib.auth.models import User
from django.db import migrations
from django.db.backends.postgresql.schema import DatabaseSchemaEditor
from django.db.migrations.state import StateApps

import google.auth
from google.cloud import secretmanager


def create_admin_superuser(apps: StateApps, schema_editor: DatabaseSchemaEditor) -> None:
    """
    Dynamically create an admin user as part of a migration
    Password is pulled from Secret Manger (previously created as part of tutorial)
    """
    if os.environ.get("CICD", None) or os.environ.get("LOCAL_DEV", None):
        # We are in CI, so just create a placeholder user for unit testing.
        admin_password = "mySuperSecretPassword!"
    else:
        client = secretmanager.SecretManagerServiceClient()

        # Get project value for identifying current context
        _, project = google.auth.default()

        # Retrieve the previously stored admin password
        PASSWORD_NAME = os.environ.get("PASSWORD_NAME", "django_admin_password")
        name = f"projects/{project}/secrets/{PASSWORD_NAME}/versions/latest"
        admin_password = client.access_secret_version(name=name).payload.data.decode(
            "UTF-8"
        )

    # Create a new user using acquired password, stripping any accidentally stored newline characters
    User.objects.create_superuser("admin", password=admin_password.strip())


class Migration(migrations.Migration):

    initial = True
    dependencies = []
    operations = [migrations.RunPython(create_admin_superuser)]
