from rest_framework import serializers

from apps.applications.models import Equipment


class EquipmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['id', 'name', 'description']