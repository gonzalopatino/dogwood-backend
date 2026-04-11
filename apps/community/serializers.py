# DRF serializers for SupportResource.
from rest_framework import serializers

from apps.community.models import SupportResource


class SupportResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportResource
        fields = "__all__"
        read_only_fields = [field.name for field in SupportResource._meta.fields]
