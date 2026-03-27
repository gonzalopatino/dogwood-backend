"""
Smoke tests — verify the app starts and basic endpoints respond.
These exist so CI has something to run on day one.
"""

import pytest
from django.test import Client


@pytest.mark.django_db
def test_admin_login_page_loads():
    """The Django Admin login page should return HTTP 200."""
    client = Client()
    response = client.get("/admin/login/")
    assert response.status_code == 200


def test_health_placeholder():
    """Placeholder — will be replaced with a real /api/v1/health/ test later."""
    assert True
