from rest_framework import serializers

from apps.applications.models import Specialty


class SpecialtyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ['name', ]