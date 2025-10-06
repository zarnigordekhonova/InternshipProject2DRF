from django.utils.translation import gettext as _

from rest_framework import serializers

from apps.applications.models import SpecialistsRequired, Specialty, Specialist
from apps.applications.api_endpoints.SpecialistList.serializers import SpecialistListSerializer
from apps.applications.api_endpoints.SpecialtyList.serializers import SpecialtyListSerializer


class SpecialistRequiredUpdateSerializer(serializers.ModelSerializer):
    specialty_input_info = serializers.CharField(write_only=True, required=False)
    specialist_input_info = serializers.CharField(write_only=True, required=False)
    
    specialty = SpecialtyListSerializer(read_only=True)
    required_specialists = SpecialistListSerializer(read_only=True)
    
    class Meta:
        model = SpecialistsRequired
        fields = [
            'id',
            'specialty',
            'specialty_input_info',  # Ixtisoslik nomi 
            'required_specialists',
            'specialist_input_info',  # Mutaxassis lavozimi nomi
            'min_count'
        ]
    
    def update(self, instance, validated_data):
        if 'specialty_input_info' in validated_data:
            specialty_name = validated_data.pop("specialty_input_info")
            try:
                specialty = Specialty.objects.get(name=specialty_name)
                instance.specialty = specialty
            except Specialty.DoesNotExist:
                raise serializers.ValidationError({
                    "specialty_input_info": _("Bunday nomdagi ixtisoslik turi mavjud emas.")
                })
            except Specialty.MultipleObjectsReturned:
                raise serializers.ValidationError({
                    "specialty_input_info": _("Bunday nomda bir nechta ixtisoslik mavjud, aniq nom kiriting.")
                })
        
        if 'specialist_input_info' in validated_data:
            specialist_title = validated_data.pop("specialist_input_info")
            try:
                specialist = Specialist.objects.get(title=specialist_title)
                instance.required_specialists = specialist
            except Specialist.DoesNotExist:
                raise serializers.ValidationError({
                    "specialist_input_info": _("Bunday lavozimli mutaxassis mavjud emas.")
                })
            except Specialist.MultipleObjectsReturned:
                raise serializers.ValidationError({
                    "specialist_input_info": _("Bunday lavozimda bir nechta mutaxassis mavjud, aniq lavozim kiriting.")
                })
        
        if 'min_count' in validated_data:
            instance.min_count = validated_data['min_count']
        
        instance.save()
        return instance



