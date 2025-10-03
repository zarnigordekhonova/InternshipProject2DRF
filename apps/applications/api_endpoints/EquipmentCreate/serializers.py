from rest_framework import serializers

from apps.applications.models import Equipment


class EquipmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['name', 'description']