from django.utils.translation import gettext as _

from rest_framework import serializers
from apps.applications.models import Branch, District


class BranchUpdateGetDistrictDataSerializer(serializers.ModelSerializer):
    class Meta:
        model =  District
        fields = ["district_name", "region"]


class BranchUpdateSerializer(serializers.ModelSerializer):
    district_input = serializers.CharField(write_only=True, source="district", required=False) 
    region = serializers.CharField(read_only=True, source='district.region.region_name')
    district_name = serializers.CharField(read_only=True, source='district.district_name')
    
    class Meta:
        model = Branch
        fields = (
            "region",
            "district_input", # kiritish uchun
            "district_name",  # ma'lumotni chiqarish uchun
            "branch_name",
        )
    
        extra_kwargs = {
            'branch_name': {'required': False}
        }

    def update(self, instance, validated_data):
        district_name_str = validated_data.pop("district", None)

        if district_name_str is not None:
            try: 
                district = District.objects.get(district_name=district_name_str)
            except District.DoesNotExist:
                raise serializers.ValidationError({"district_input": _("Bunday nomdagi tuman mavjud emas.")})
            except District.MultipleObjectsReturned:
                raise serializers.ValidationError({"district_input": _("Bunday nomda bir nechta tuman mavjud, aniq nom kiriting.")})
            
            instance.district = district
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            
        instance.save()
        return instance