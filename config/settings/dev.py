"""
Development settings — used when running locally with docker-compose.
"""

from .base import *  # noqa: F401, F403

DEBUG = True

ALLOWED_HOSTS = ["*"]
