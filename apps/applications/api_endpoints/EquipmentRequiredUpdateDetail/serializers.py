from rest_framework import serializers

from apps.applications.models import EquipmentRequiredItem, EquipmentRequired, Specialty, Equipment


class EquipmentRequiredItemUpdateSerializer(serializers.ModelSerializer):
    specialty = serializers.CharField(write_only=True, required=False)
    equipment_name = serializers.CharField(write_only=True, required=False)

    specialty_display = serializers.CharField(source="equipment_required.specialty.name", read_only=True)
    equipment_display = serializers.CharField(source="equipment.name", read_only=True)

    class Meta:
        model = EquipmentRequiredItem
        fields = ["id", "specialty", "equipment_name", "min_count", "specialty_display", "equipment_display"]

    def validate(self, attrs):
        specialty_name = attrs.get("specialty")
        equipment_name = attrs.get("equipment_name")

        if specialty_name:
            try:
                specialty = Specialty.objects.get(name=specialty_name)
            except Specialty.DoesNotExist:
                raise serializers.ValidationError(
                {"specialty": f"'{specialty_name}' nomdagi ixtisoslik mavjud emas."}
            )
        
            except Specialty.MultipleObjectsReturned:
                raise serializers.ValidationError({
                "specialty": f"'{specialty_name}' nomli bir nechta ixtisoslik mavjud. Iltimos, aniq nom kiriting."
            })
            equipment_required, _ = EquipmentRequired.objects.get_or_create(specialty=specialty)
            attrs["equipment_required"] = equipment_required

        if equipment_name:
            try:
                equipment = Equipment.objects.get(name=equipment_name)
            except Equipment.DoesNotExist:
                raise serializers.ValidationError(
                {"equipment_name": f"'{equipment_name}' nomdagi jihoz mavjud emas."}
            )
            except Equipment.MultipleObjectsReturned:
                raise serializers.ValidationError({
                "equipment_name": f"'{equipment_name}' nomli bir nechta jihoz mavjud. Iltimos, aniq nom kiriting."
            })

            attrs["equipment"] = equipment

        return attrs

    def update(self, instance, validated_data):
        validated_data.pop("specialty", None)
        validated_data.pop("equipment_name", None)
        return super().update(instance, validated_data)
