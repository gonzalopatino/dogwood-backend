from django.urls import path  # noqa: F401
from .views import PageListView, PageView

urlpatterns = [
    path('pages/', PageListView.as_view(), name='page-list'),
    path('pages/<slug:slug>/', PageView.as_view(), name='page')

]
