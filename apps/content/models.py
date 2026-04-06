"""
Content app models: Page, Post, and Attachment.

These three models store all the main content for the Dogwood website.
Think of it this way:
  - Page = a static page like "Insurance" or "Code of Conduct"
  - Post = a news/events blog entry like "Drama Club Presents"
  - Attachment = a downloadable file (PDF, image) linked to a Page or Post
"""

from django.conf import settings
from django.db import models


class Page(models.Model):
    """
    A static content page.

    On the current WordPress site, these are the items in the top navigation:
    Welcome, Board, Activities, Insurance, Constitution, Code of Conduct, etc.

    Each page is a scrollable block of rich-text content (HTML) with optional
    downloadable attachments (PDFs, images).

    The `status` field controls visibility:
      - "draft" = only visible in Django Admin (staff working on it)
      - "published" = visible to the public via the API

    The `display_order` field controls the order pages appear in the
    site navigation. Lower numbers appear first.
    """

    # STATUS_CHOICES defines the allowed values for the `status` field.
    # Each tuple is (database_value, human_readable_label).
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
    ]

    # CharField = short text. max_length is required by Django.
    title = models.CharField(max_length=200)

    # SlugField = URL-friendly string (lowercase, hyphens, no spaces).
    # Example: "Code of Conduct" → slug = "code-of-conduct"
    # unique=True means no two pages can have the same slug.
    # help_text shows up as a hint in Django Admin.
    slug = models.SlugField(
        max_length=200,
        unique=True,
        help_text="URL-friendly identifier, e.g. 'insurance'",
    )

    # TextField = unlimited text. We store HTML here because the content
    # includes formatted text, embedded images, links, etc.
    body = models.TextField(help_text="Rich-text content (HTML)")

    # CharField with choices = dropdown in Django Admin.
    # Default is "draft" so new pages don't accidentally go live.
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")

    # PositiveIntegerField = a whole number >= 0.
    # Used to control the order pages appear in the site navigation.
    display_order = models.PositiveIntegerField(
        default=0,
        help_text="Controls the order pages appear in navigation. Lower = first.",
    )

    # auto_now_add=True means Django sets this once when the record is created.
    created_at = models.DateTimeField(auto_now_add=True)

    # auto_now=True means Django updates this every time the record is saved.
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Default ordering when you query Page.objects.all()
        # First by display_order (ascending), then alphabetically by title.
        ordering = ["display_order", "title"]

    def __str__(self):
        # This controls what the page looks like in Django Admin dropdowns
        # and list views. Just show the title.
        return self.title


class Post(models.Model):
    """
    A News & Events blog post.

    On the current WordPress site, these are the entries on the "News & Events"
    page: Drama Club announcements, AGM notices, Honour Roll nominations,
    Olympic viewing events, wellness workshops, etc.

    Posts are displayed in reverse chronological order (newest first).

    The `status` field has three options:
      - "draft" = work in progress, not public
      - "published" = live on the site
      - "archived" = no longer shown publicly but kept in the database
    """

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("published", "Published"),
        ("archived", "Archived"),
    ]

    title = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300, unique=True)
    body = models.TextField(help_text="Rich-text content (HTML)")

    # ImageField is like FileField but validates that the upload is an image.
    # upload_to defines the folder structure in storage (local or S3).
    # %Y/%m/ creates year/month subfolders: posts/images/2026/03/photo.jpg
    # blank=True means this field is optional.
    featured_image = models.ImageField(upload_to="posts/images/%Y/%m/", blank=True)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")

    # When this post was published (or should be published).
    # null=True means the database column allows NULL.
    # blank=True means the form field is optional.
    published_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="When this post goes live",
    )

    # ForeignKey = a link to another model (the User who wrote this post).
    # on_delete=SET_NULL means if the user is deleted, the post stays but
    # the author field becomes NULL (instead of deleting the post too).
    # related_name="posts" lets you do user.posts.all() to get all posts by a user.
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Newest posts first (the minus sign means descending order)
        ordering = ["-published_at"]

    def __str__(self):
        return self.title


class Attachment(models.Model):
    """
    A downloadable file attached to a Page or Post.

    Examples from the current site:
      - AGM agenda PDF attached to the "AGM Notice" post
      - Nomination form PDF attached to the "Honour Roll" post
      - Weekly cafe menu PDF attached to the "Welcome" page
      - Event poster image attached to an event post

    An attachment belongs to either a Page or a Post, but not both.
    We use two nullable ForeignKeys for this (one will always be NULL).
    """

    title = models.CharField(max_length=200)

    # FileField stores the path to the uploaded file.
    # In development, files go to the local media/ folder.
    # In production, django-storages sends them to S3.
    file = models.FileField(upload_to="attachments/%Y/%m/")

    # Controls the order attachments appear on a page/post.
    display_order = models.PositiveIntegerField(default=0)

    # An attachment belongs to ONE of these (the other is NULL).
    # on_delete=CASCADE means if the parent Page/Post is deleted,
    # its attachments are deleted too.
    # related_name="attachments" lets you do page.attachments.all()
    page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="attachments",
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="attachments",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return self.title
