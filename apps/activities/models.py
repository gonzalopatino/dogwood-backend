# Models for Categories and ActivityGroups.
# To be implemented in Week 3.
"""
Activities app models: Category and ActivityGroup.

Dogwood Pavilion hosts 50+ activity groups. Each group belongs to
one of three categories. Each group has a volunteer leader who
coordinates the activity and serves as the contact person.
"""

from django.db import models


class Category(models.Model):
    """
    Activity group category.

    There are exactly three categories (matching the current site):
      - "Social, Educational & Cultural" (slug: social)
      - "Art, Craft & Games" (slug: arts)
      - "Sports & Athletics" (slug: sports)

    These are created once in Django Admin and rarely change.
    The slug is used for filtering in the API: /api/v1/activities/?category=sports
    """

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        # "categories" instead of the default "categorys"
        verbose_name_plural = "categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class ActivityGroup(models.Model):
    """
    One of the 50+ activity groups at Dogwood Pavilion.

    Examples: Drama Club, Lapidary Workshop, Table Tennis, Snooker,
    Bridge, Quilting, Book Club, Badminton, Floor Curling.

    Each group has:
      - A category (FK to Category)
      - A description of the activity
      - A schedule (when it meets)
      - A location (where in the pavilion)
      - Leader contact info (name, phone, email)

    The leader fields are simple text fields (not a FK to a User model)
    because group leaders don't log in to the system. Staff enter their
    contact info manually through Django Admin.
    """

    name = models.CharField(max_length=200)

    # ForeignKey = "this group belongs to one category"
    # on_delete=CASCADE = if a category is deleted, all its groups are deleted too
    # related_name="groups" = you can do category.groups.all() to get all groups in a category
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="groups")

    description = models.TextField(blank=True, help_text="Rich-text description (HTML)")

    # Schedule is free-text because formats vary widely:
    # "Wednesdays 1:00 p.m. - 3:00 p.m." or "Daily" or "1st Monday of the month"
    schedule = models.CharField(max_length=300, blank=True, help_text="e.g. 'Wednesdays 1:00 p.m. - 3:00 p.m.'")

    location = models.CharField(max_length=200, blank=True, help_text="Room or area within Dogwood Pavilion")

    # Leader contact info — all optional because some groups may not have a leader listed yet
    leader_name = models.CharField(max_length=200, blank=True)
    leader_phone = models.CharField(max_length=30, blank=True)
    leader_email = models.EmailField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Sort by category first, then alphabetically within each category
        ordering = ["category", "name"]

    def __str__(self):
        return self.name
