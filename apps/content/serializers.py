# DRF serializers for Pages, Posts, Attachments.
# To be implemented in Week 3.
from rest_framework import serializers
from .models import Page, Attachment


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['title', 'file', 'display_order']

class PageSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many = True)
    class Meta:
        model = Page
        fields = ['title', 'slug','body','attachments']
        

class PageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['title', 'slug', 'display_order']
