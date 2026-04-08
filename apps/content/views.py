# API views for public read-only content endpoints.
# To be implemented in Week 3.
from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Page, Post
from .serializers import PageListSerializer, PageSerializer, PostListSerializer, PostSerializer


## -- Pages -- ##
# This endpoint is get one page by it's slug.
class PageView(RetrieveAPIView):
    serializer_class = PageSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Page.objects.filter(status="published")


# This endpoint is list all published pages
class PageListView(ListAPIView):
    serializer_class = PageListSerializer

    def get_queryset(self):
        return Page.objects.filter(status="published")


## -- Posts -- ##
class PostView(RetrieveAPIView):
    serializer_class = PostSerializer
    lookup_field = "slug"

    def get_queryset(self):
        return Post.objects.filter(status="published")


class PostListView(ListAPIView):
    serializer_class = PostListSerializer

    def get_queryset(self):
        return Post.objects.filter(status="published")
