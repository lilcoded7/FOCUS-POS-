"""
Django settings for setup project (desktop app version).
"""

from pathlib import Path
import os
import sys

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key secret in production!
SECRET_KEY = "django-insecure-laq8j$%vq-yn8gi@oweq_z4%)jkc#(dcujw+c!^7&%dvb392l-"

# For development/desktop packaging, keep True. Switch to False for production builds.
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "accounts",
    "shop",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "setup.urls"

WHITENOISE_USE_FINDERS = True

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "setup.wsgi.application"

# Custom user model
AUTH_USER_MODEL = "accounts.User"

# ---------------------------
# Database (SQLite portable)
# ---------------------------
# Default: project-level DB (for development)
db_path = BASE_DIR / "db.sqlite3"

# Detect if running from PyInstaller bundle
if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    # Use user’s home directory for persistence
    user_data_dir = Path.home() / ".my_django_app"
    user_data_dir.mkdir(parents=True, exist_ok=True)
    db_path = user_data_dir / "db.sqlite3"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": str(db_path),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Authentication backends
AUTHENTICATION_BACKENDS = [
    "accounts.backends.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ---------------------------
# Static & Media files
# ---------------------------
STATIC_URL = "/static/"
MEDIA_URL = "/media/"

# Default (dev mode)
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_ROOT = BASE_DIR / "media"

# In frozen mode, put static & media in user_data_dir too
if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    STATIC_ROOT = user_data_dir / "staticfiles"
    MEDIA_ROOT = user_data_dir / "media"
    STATICFILES_DIRS = []  # no extra dirs in frozen mode

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------
# Email config
# ---------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = "tulasijoshuambawini@gmail.com"
EMAIL_HOST_PASSWORD = "ywyw cupx gfkp jtip"
