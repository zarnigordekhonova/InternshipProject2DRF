from rest_framework import serializers

from apps.applications.models import SpecialistsRequired, Specialty, Specialist
from apps.applications.api_endpoints.SpecialtyList.serializers import SpecialtyListSerializer
from apps.applications.api_endpoints.SpecialistList.serializers import SpecialistListSerializer


class SpecialistRequiredCreateSerializer(serializers.ModelSerializer):
    specialty_input_info = serializers.CharField(write_only=True)
    specialist_input_info = serializers.CharField(write_only=True)
    
    specialty = SpecialtyListSerializer(read_only=True)
    required_specialists = SpecialistListSerializer(read_only=True)
    
    class Meta:
        model = SpecialistsRequired
        fields = [
            'id',
            'specialty',
            'specialty_input_info',  # Ixtisoslik nomi
            'required_specialists',
            'specialist_input_info',  # Mutaxassis lavozimi
            'min_count'
        ]
    
    def create(self, validated_data):
        specialty_name = validated_data.pop("specialty_input_info")
        specialist_title = validated_data.pop("specialist_input_info")
        
        # Mutaxassislik nomini olish
        try:
            specialty = Specialty.objects.get(name=specialty_name)
        except Specialty.DoesNotExist:
            raise serializers.ValidationError({
                "specialty_input_info": "Bunday nomdagi ixtisoslik turi mavjud emas."
            })
        except Specialty.MultipleObjectsReturned:
            raise serializers.ValidationError({
                "specialty_input_info": "Bunday nomda bir nechta ixtisoslik mavjud, aniq nom kiriting."
            })
        
        # Mutaxassis nomini olish
        try:
            specialist = Specialist.objects.get(title=specialist_title)
        except Specialist.DoesNotExist:
            raise serializers.ValidationError({
                "specialist_input_info": "Bunday lavozimli mutaxassis mavjud emas."
            })
        except Specialist.MultipleObjectsReturned:
            raise serializers.ValidationError({
                "specialist_input_info": "Bunday lavozimda bir nechta mutaxassis mavjud, aniq lavozim kiriting."
            })
        
        sp_required = SpecialistsRequired.objects.create(
            specialty=specialty,
            required_specialists=specialist,
            **validated_data
        )
        
        return sp_required
