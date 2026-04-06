# Models for BoardMember, ContactSubmission, EmailSubscription.
# To be implemented in Week 3.

"""
Info app models — BoardMember.

Covers SRS requirement:
  FR-14: Store Board Members with name, position, photo, term year, is_current flag.

NOTE TO DEVELOPER D:
  You will add ContactSubmission and EmailSubscription models to this
  file BELOW the BoardMember class after this PR is merged.
  Do not modify the BoardMember model.
"""

from django.db import models


class BoardMember(models.Model):
    """
    A member of the Dogwood Pavilion Advisory Board.

    Real examples from the current site (2025-2026 board):
      - Wilhelmina Martin — President
      - Bob Willems — First Vice President
      - Harjit Nijjar — Financial Director
      - Bob Briggs — Assistant Financial Director

    The is_current field controls visibility in the public API:
      - True  → shown on the Board page (GET /api/v1/board/)
      - False → hidden from the public but kept in database for records

    When a new board is elected each year, staff set the old members
    to is_current=False and create new entries for the new board.

    display_order controls the order members appear on the page.
    President should be 1, VP should be 2, etc.
    """

    # The member's full name as it should appear on the website.
    name = models.CharField(max_length=200)

    # Their role on the board.
    # help_text shows up as a hint below the field in Django Admin.
    position = models.CharField(
        max_length=200,
        help_text="e.g. 'President', 'First Vice President', 'Director at Large'",
    )

    # ImageField stores the path to an uploaded photo.
    # upload_to defines the folder: board/photos/
    # blank=True means a photo is optional (not all members have one).
    photo = models.ImageField(upload_to="board/photos/", blank=True)

    # The board term, e.g. "2025-2026".
    # CharField (not DateField) because terms are expressed as year ranges.
    term_year = models.CharField(max_length=20, help_text="e.g. '2025-2026'")

    # Controls whether this member appears in the public API.
    # BooleanField renders as a checkbox in Django Admin.
    is_current = models.BooleanField(default=True)

    # Controls display order. Lower numbers appear first.
    # President = 1, VP = 2, Secretary = 3, etc.
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "name"]

    def __str__(self):
        # Shows "Wilhelmina Martin — President" in Admin list views
        return f"{self.name} — {self.position}"
