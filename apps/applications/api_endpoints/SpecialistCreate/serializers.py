from rest_framework import serializers

from apps.applications.models import Specialist


class SpecialistCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialist
        fields = ['title', ]
