from rest_framework import serializers

from apps.applications.models import Specialist


class SpecialistListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialist
        fields = ['id', 'title',]