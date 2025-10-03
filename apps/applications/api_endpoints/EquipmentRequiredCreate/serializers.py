from rest_framework import serializers

from apps.applications.models import EquipmentRequiredItem, EquipmentRequired, Specialty, Equipment


class EquipmentRequiredItemCreateSerializer(serializers.ModelSerializer):
    specialty = serializers.CharField(write_only=True)
    equipment_name = serializers.CharField(write_only=True)

    class Meta:
        model = EquipmentRequiredItem
        fields = ["specialty", "equipment_name", "min_count"]

    def validate(self, attrs):
        specialty_name = attrs.get("specialty")
        equipment_name = attrs.get("equipment_name")

        # Ixtisoslik nomini olish va tekshirish
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

        # Jihoz nomini olish va tekshirish
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

        attrs["equipment_required"] = equipment_required
        attrs["equipment"] = equipment
        return attrs

    def create(self, validated_data):
        validated_data.pop("specialty")
        validated_data.pop("equipment_name")
        return super().create(validated_data)
    

# Agar bitta requestda bir nechta jihoz obyektlari kelsa, shularni chiqarish uchun quuyidagi
# serializer ishlatiladi.
class EquipmentRequiredItemDetailSerializer(serializers.ModelSerializer):
    specialty = serializers.CharField(source="equipment_required.specialty.name", read_only=True)
    equipment_name = serializers.CharField(source="equipment.name", read_only=True)

    class Meta:
        model = EquipmentRequiredItem
        fields = ["id", "specialty", "equipment_name", "min_count"]