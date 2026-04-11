from django.urls import path  # noqa: F401

from apps.community.views import SupportResourceListView

urlpatterns = [path("community/", SupportResourceListView.as_view())]
