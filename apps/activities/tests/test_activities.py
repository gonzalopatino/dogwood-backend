import pytest
from django.test import Client

from apps.activities.models import ActivityGroup, Category


@pytest.fixture
def categories(db):
    social = Category.objects.create(name="Social, Educational & Cultural", slug="social")
    arts = Category.objects.create(name="Art, Craft & Games", slug="arts")
    sports = Category.objects.create(name="Sports & Athletics", slug="sports")
    return {"social": social, "arts": arts, "sports": sports}


@pytest.fixture
def activity_groups(db, categories):
    drama = ActivityGroup.objects.create(
        name="Drama Club",
        category=categories["social"],
        description="Perform plays and skits.",
        schedule="Tuesdays 1:00 p.m. - 3:00 p.m.",
        leader_name="Jane Smith",
        leader_phone="604-555-0001",
        leader_email="jane@example.com",
    )
    snooker = ActivityGroup.objects.create(
        name="Snooker",
        category=categories["sports"],
        description="Drop-in snooker.",
        schedule="Daily",
        leader_name="Bob Jones",
        leader_phone="604-555-0002",
    )
    # Group with no leader
    lapidary = ActivityGroup.objects.create(
        name="Lapidary Workshop",
        category=categories["arts"],
        description="Rock cutting and polishing.",
    )
    return {"drama": drama, "snooker": snooker, "lapidary": lapidary}


@pytest.mark.django_db
class TestActivityGroupAPI:
    def test_list_all_activities(self, activity_groups):
        client = Client()
        response = client.get("/api/v1/activities/")
        assert response.status_code == 200
        assert len(response.json()["results"]) == 3

    def test_filter_by_category(self, activity_groups):
        client = Client()
        response = client.get("/api/v1/activities/?category=sports")
        assert response.status_code == 200
        names = [g["name"] for g in response.json()["results"]]
        assert names == ["Snooker"]

    def test_filter_invalid_category_returns_empty(self, activity_groups):
        client = Client()
        response = client.get("/api/v1/activities/?category=nonexistent")
        assert response.status_code == 200
        assert len(response.json()["results"]) == 0


@pytest.mark.django_db
class TestActivityLeadersAPI:
    def test_leaders_excludes_groups_without_leader(self, activity_groups):
        client = Client()
        response = client.get("/api/v1/activities/leaders/")
        assert response.status_code == 200
        names = [g["leader_name"] for g in response.json()]
        assert "Jane Smith" in names
        assert "Bob Jones" in names
        # Lapidary has no leader, should not appear
        group_names = [g["group_name"] for g in response.json()]
        assert "Lapidary Workshop" not in group_names

    def test_leaders_not_paginated(self, activity_groups):
        client = Client()
        response = client.get("/api/v1/activities/leaders/")
        # Should be a plain list, not a paginated response with "results" key
        assert isinstance(response.json(), list)
