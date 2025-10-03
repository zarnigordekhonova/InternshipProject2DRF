from rest_framework import serializers

from apps.applications.models import EquipmentRequiredItem


class EquipmentRequiredItemListSerializer(serializers.ModelSerializer):
    specialty = serializers.CharField(source="equipment_required.specialty.name", read_only=True)
    equipment_name = serializers.CharField(source="equipment.name", read_only=True)

    class Meta:
        model = EquipmentRequiredItem
        fields = ["id", "specialty", "equipment_name", "min_count"]