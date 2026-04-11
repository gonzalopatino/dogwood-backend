# API views for community support directory.
from rest_framework.generics import ListAPIView

from apps.community.models import SupportResource
from apps.community.serializers import SupportResourceSerializer


class SupportResourceListView(ListAPIView):
    queryset = SupportResource.objects.all()
    serializer_class = SupportResourceSerializer
