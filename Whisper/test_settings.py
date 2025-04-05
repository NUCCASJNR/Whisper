# test_settings.py

from .settings import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Disable migrations during tests
MIGRATION_MODULES = {app: None for app in INSTALLED_APPS}
