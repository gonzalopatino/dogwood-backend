from django.urls import path  # noqa: F401

from .views import PageListView, PageView, PostListView, PostView

urlpatterns = [
    path('pages/', PageListView.as_view(), name='page-list'),
    path('pages/<slug:slug>/', PageView.as_view(), name='page'),
    path('posts/', PostListView.as_view(), name='post-list' ),
    path('posts/<slug:slug>/', PostView.as_view(), name='post'),
]
