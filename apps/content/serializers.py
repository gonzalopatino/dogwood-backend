# DRF serializers for Pages, Posts, Attachments.
# To be implemented in Week 3.
from rest_framework import serializers

from .models import Attachment, Page, Post


## -- Pages -- ##
# This set the attachment for PageSerializer to get the attachments list
class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['title', 'file', 'display_order']

class PageSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many = True, read_only = True)
    class Meta:
        model = Page
        fields = ['title', 'slug','body','attachments']
        

class PageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['title', 'slug', 'display_order']


## -- Posts -- ##
class PostSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many = True, read_only = True)
    class Meta:
        model = Post
        fields = ['title', 'slug','body','attachments']
        
        
class PostListSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many = True ,read_only = True)
    class Meta:
        model = Post
        fields = ['title', 'slug', 'body', 'published_at', 'attachments']
