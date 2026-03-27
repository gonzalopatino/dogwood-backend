"""
Shared settings for all environments.
"""

import os
from pathlib import Path

# ─── Paths ───────────────────────────────────────────────
# BASE_DIR points to the project root (dogwood-backend/)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ─── Security ────────────────────────────────────────────
# NEVER hardcode this. It comes from environment variables.
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "change-me-in-production")

# ─── Application Definition ─────────────────────────────
INSTALLED_APPS = [
    # Django built-in apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party apps
    "rest_framework",
    # Our apps
    "apps.content",
    "apps.activities",
    "apps.community",
    "apps.info",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "config.wsgi.application"

# ─── Database ────────────────────────────────────────────
# Default to PostgreSQL. Connection details come from environment variables.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "dogwood"),
        "USER": os.environ.get("DB_USER", "dogwood"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "dogwood"),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "5432"),
    }
}

# ─── Password Validation ────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ─── Password Hashing ───────────────────────────────────
# bcrypt first (strongest), with fallbacks for existing hashes
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
]

# ─── Internationalization ────────────────────────────────
LANGUAGE_CODE = "en-ca"
TIME_ZONE = "America/Vancouver"
USE_I18N = True
USE_TZ = True

# ─── Static Files ────────────────────────────────────────
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# ─── Media Files ─────────────────────────────────────────
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ─── Django REST Framework ───────────────────────────────
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}

# ─── Default Auto Field ─────────────────────────────────
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
