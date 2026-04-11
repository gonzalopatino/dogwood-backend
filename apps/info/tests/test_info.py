import uuid

import pytest
from apps.info.models import BoardMember, ContactSubmission, EmailSubscription
from django.test import Client


@pytest.fixture
def board_members(db):
    BoardMember.objects.create(name="Wilhelmina Martin", position="President", term_year="2025-2026", is_current=True)
    BoardMember.objects.create(
        name="Bob Willems", position="First Vice President", term_year="2025-2026", is_current=True
    )
    BoardMember.objects.create(name="Past Member", position="Secretary", term_year="2023-2024", is_current=False)


# ─── Board Tests ─────────────────────────────────────────


@pytest.mark.django_db
class TestBoardAPI:
    def test_list_current_board_only(self, board_members):
        client = Client()
        response = client.get("/api/v1/board/")
        assert response.status_code == 200
        names = [m["name"] for m in response.json()]
        assert "Wilhelmina Martin" in names
        assert "Past Member" not in names

    def test_board_not_paginated(self, board_members):
        client = Client()
        response = client.get("/api/v1/board/")
        assert isinstance(response.json(), list)


# ─── Contact Form Tests ─────────────────────────────────


@pytest.mark.django_db
class TestContactAPI:
    def test_submit_contact_form(self):
        client = Client()
        response = client.post(
            "/api/v1/contact/",
            data={"name": "John Doe", "email": "john@example.com", "message": "Hello!"},
            content_type="application/json",
        )
        assert response.status_code == 201
        assert ContactSubmission.objects.count() == 1
        submission = ContactSubmission.objects.first()
        assert submission.name == "John Doe"
        assert submission.is_reviewed is False

    def test_submit_contact_form_missing_fields(self):
        client = Client()
        response = client.post(
            "/api/v1/contact/",
            data={"name": "John Doe"},
            content_type="application/json",
        )
        assert response.status_code == 400

    def test_submit_contact_form_optional_phone(self):
        client = Client()
        response = client.post(
            "/api/v1/contact/",
            data={"name": "Jane", "email": "jane@example.com", "phone": "604-555-0000", "message": "Hi there"},
            content_type="application/json",
        )
        assert response.status_code == 201
        assert ContactSubmission.objects.first().phone == "604-555-0000"


# ─── Email Subscription Tests ────────────────────────────


@pytest.mark.django_db
class TestSubscriptionAPI:
    def test_subscribe_new_email(self):
        client = Client()
        response = client.post(
            "/api/v1/subscribe/",
            data={"email": "reader@example.com"},
            content_type="application/json",
        )
        assert response.status_code == 201
        sub = EmailSubscription.objects.get(email="reader@example.com")
        assert sub.is_verified is False
        assert sub.verification_token is not None

    def test_subscribe_duplicate_unverified_returns_200(self):
        EmailSubscription.objects.create(email="reader@example.com", is_verified=False)
        client = Client()
        response = client.post(
            "/api/v1/subscribe/",
            data={"email": "reader@example.com"},
            content_type="application/json",
        )
        assert response.status_code == 200

    def test_subscribe_duplicate_verified_returns_200(self):
        EmailSubscription.objects.create(email="reader@example.com", is_verified=True)
        client = Client()
        response = client.post(
            "/api/v1/subscribe/",
            data={"email": "reader@example.com"},
            content_type="application/json",
        )
        assert response.status_code == 200
        assert "Already subscribed" in response.json()["detail"]

    def test_verify_subscription(self):
        sub = EmailSubscription.objects.create(email="reader@example.com", is_verified=False)
        client = Client()
        response = client.get(f"/api/v1/subscribe/verify/{sub.verification_token}/")
        assert response.status_code == 200
        sub.refresh_from_db()
        assert sub.is_verified is True

    def test_verify_invalid_token(self):
        client = Client()
        fake_token = uuid.uuid4()
        response = client.get(f"/api/v1/subscribe/verify/{fake_token}/")
        assert response.status_code == 404

    def test_unsubscribe(self):
        sub = EmailSubscription.objects.create(email="reader@example.com", is_verified=True)
        client = Client()
        response = client.get(f"/api/v1/subscribe/unsubscribe/{sub.verification_token}/")
        assert response.status_code == 200
        sub.refresh_from_db()
        assert sub.is_verified is False
        assert sub.unsubscribed_at is not None


# ─── Health Check Tests ──────────────────────────────────


@pytest.mark.django_db
class TestHealthCheck:
    def test_health_returns_200(self):
        client = Client()
        response = client.get("/api/v1/health/")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
