# Django Admin configuration for Pages, Posts, Attachments.
# To be implemented in Week 3.
from django.contrib import admin  # noqa: F401

from .models import Attachment, Page, Post

admin.site.register(Page)
admin.site.register(Post)
admin.site.register(Attachment)
