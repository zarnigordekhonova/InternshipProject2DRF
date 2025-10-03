from rest_framework import serializers

from apps.applications.models import Specialty


class SpecialtyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ['id', 'name']