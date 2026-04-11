import pytest
from apps.community.models import SupportResource
from django.test import Client


@pytest.fixture
def resources(db):
    SupportResource.objects.create(
        org_name="BC Seniors Line",
        description="Information on provincial services.",
        phone="1-800-465-4911",
        schedule="24 Hours a Day",
    )
    SupportResource.objects.create(
        org_name="Stroke Recovery Branch",
        description="Support and activities for those recovering from stroke.",
        phone="604-927-6093",
        schedule="Fridays 10:30 a.m. - 2:00 p.m.",
    )


@pytest.mark.django_db
class TestCommunityAPI:
    def test_list_resources(self, resources):
        client = Client()
        response = client.get("/api/v1/community/")
        assert response.status_code == 200
        assert len(response.json()["results"]) == 2

    def test_resource_fields(self, resources):
        client = Client()
        response = client.get("/api/v1/community/")
        first = response.json()["results"][0]
        assert "org_name" in first
        assert "phone" in first
        assert "schedule" in first
