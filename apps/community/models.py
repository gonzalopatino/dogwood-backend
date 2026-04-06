"""
Community app models: SupportResource.

Covers SRS requirement:
  FR-12: Store Community Support resources with org name, description,
         phone, email, address, website, schedule.

On the current WordPress site, the "Community Support" page lists
local organizations that help seniors: Arthritis Support Group,
Alzheimer Society, BC Seniors Line, Fraser Health Crisis Line,
Stroke Recovery Branch, Tri-Cities Better at Home, etc.

Each entry has contact details and a schedule. Staff manage these
through Django Admin.
"""

from django.db import models


class SupportResource(models.Model):
    """
    A community support resource listed on the Community Support page.

    Real examples from the current site:
      - "BC Seniors Line" — phone: 1-800-465-4911, schedule: "24 Hours a Day"
      - "Stroke Recovery Branch" — phone: 604-927-6093, schedule: "Fridays 10:30 a.m. - 2:00 p.m."
      - "Fraser Health Crisis Line" — phone: 604-951-8855, schedule: "24/7"
      - "Tri-Cities Better at Home" — phone: 604-936-3900

    All fields except org_name are optional because some resources
    have only a phone number, others have a website, etc.
    """

    # verbose_name overrides the label shown in Django Admin.
    # Without it, Django would show "Org name" (auto-generated from field name).
    org_name = models.CharField("Organization name", max_length=300)

    # TextField = unlimited length text, rendered as a large text area in Admin.
    description = models.TextField(blank=True)

    # CharField for phone because phone numbers can include dashes,
    # parentheses, extensions, and "1-800" prefixes — not just digits.
    phone = models.CharField(max_length=50, blank=True)

    # EmailField = CharField with email validation built in.
    email = models.EmailField(blank=True)

    address = models.CharField(max_length=300, blank=True)

    # URLField = CharField with URL validation (must start with http/https).
    website = models.URLField(blank=True)

    # Schedule is free-text because formats vary:
    # "24 Hours a Day — 7 Days a Week" vs "Fridays 10:30 a.m. - 2:00 p.m."
    schedule = models.CharField(
        max_length=300,
        blank=True,
        help_text="e.g. '24 Hours a Day — 7 Days a Week'",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Alphabetical by organization name
        ordering = ["org_name"]

    def __str__(self):
        return self.org_name
