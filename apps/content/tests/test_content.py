import pytest
from apps.content.models import Attachment, Page, Post
from django.test import Client
from django.utils import timezone


@pytest.fixture
def published_page(db):
    return Page.objects.create(
        title="Insurance",
        slug="insurance",
        body="<p>Insurance coverage details.</p>",
        status="published",
        display_order=1,
    )


@pytest.fixture
def draft_page(db):
    return Page.objects.create(
        title="Draft Page",
        slug="draft-page",
        body="<p>Not ready yet.</p>",
        status="draft",
    )


@pytest.fixture
def published_post(db):
    return Post.objects.create(
        title="Drama Club Presents",
        slug="drama-club-presents",
        body="<p>Upcoming performance details.</p>",
        status="published",
        published_at=timezone.now(),
    )


@pytest.fixture
def archived_post(db):
    return Post.objects.create(
        title="Old Event",
        slug="old-event",
        body="<p>This already happened.</p>",
        status="archived",
        published_at=timezone.now(),
    )


@pytest.fixture
def attachment(db, published_page):
    return Attachment.objects.create(
        title="Membership Form",
        file="attachments/2026/03/form.pdf",
        page=published_page,
    )


# ─── Page Tests ──────────────────────────────────────────


@pytest.mark.django_db
class TestPageAPI:
    def test_list_pages_returns_only_published(self, published_page, draft_page):
        client = Client()
        response = client.get("/api/v1/pages/")
        assert response.status_code == 200
        data = response.json()
        slugs = [p["slug"] for p in data["results"]]
        assert "insurance" in slugs
        assert "draft-page" not in slugs

    def test_get_page_by_slug(self, published_page, attachment):
        client = Client()
        response = client.get("/api/v1/pages/insurance/")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Insurance"
        assert data["slug"] == "insurance"
        assert len(data["attachments"]) == 1
        assert data["attachments"][0]["title"] == "Membership Form"

    def test_get_draft_page_returns_404(self, draft_page):
        client = Client()
        response = client.get("/api/v1/pages/draft-page/")
        assert response.status_code == 404

    def test_list_pages_ordered_by_display_order(self, db):
        Page.objects.create(title="Z Page", slug="z-page", body="", status="published", display_order=2)
        Page.objects.create(title="A Page", slug="a-page", body="", status="published", display_order=1)
        client = Client()
        response = client.get("/api/v1/pages/")
        titles = [p["title"] for p in response.json()["results"]]
        assert titles[0] == "A Page"
        assert titles[1] == "Z Page"


# ─── Post Tests ──────────────────────────────────────────


@pytest.mark.django_db
class TestPostAPI:
    def test_list_posts_returns_only_published(self, published_post, archived_post):
        client = Client()
        response = client.get("/api/v1/posts/")
        assert response.status_code == 200
        slugs = [p["slug"] for p in response.json()["results"]]
        assert "drama-club-presents" in slugs
        assert "old-event" not in slugs

    def test_get_post_by_slug(self, published_post):
        client = Client()
        response = client.get("/api/v1/posts/drama-club-presents/")
        assert response.status_code == 200
        assert response.json()["title"] == "Drama Club Presents"

    def test_get_archived_post_returns_404(self, archived_post):
        client = Client()
        response = client.get("/api/v1/posts/old-event/")
        assert response.status_code == 404
