# API views for public read-only content endpoints.
# To be implemented in Week 3.
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Page
from .serializers import PageListSerializer, PageSerializer

# This endpoint is get one page by it's slug.
class PageView(RetrieveAPIView):
  serializer_class = PageSerializer
  lookup_field = 'slug'
  
  def get_queryset(self):
    return Page.objects.filter(status='published')
  
  
  

# This endpoint is list all published pages 
class PageListView(ListAPIView):
    serializer_class = PageListSerializer

    def get_queryset(self):
        return Page.objects.filter(status='published').order_by('display_order', 'title')