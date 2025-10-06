from django.utils.translation import gettext as _

from rest_framework import serializers

from apps.applications.models import Branch, District
from apps.applications.api_endpoints.GetRegionDistrictData import GetDistrictDataSerializer, GetRegionDataSerializer


class BranchCreateSerializer(serializers.ModelSerializer):
    district_name_input = serializers.CharField(write_only=True)
    district = GetDistrictDataSerializer(read_only=True)
    
    class Meta:
        model = Branch
        fields = (
            "district_name_input",  # for entering district name
            "district",  
            "branch_name",
        )

    def create(self, validated_data):
        district = validated_data.pop("district_name_input")
        try: 
            district_name = District.objects.get(district_name=district)
        except District.DoesNotExist:
            raise serializers.ValidationError({"district": _("Bunday nomdagi tuman mavjud emas.")})
        except District.MultipleObjectsReturned:
            raise serializers.ValidationError({"district": _("Bunday nomda bir nechta tuman mavjud, aniq nom kiriting.")})
        
        branch = Branch.objects.create(district=district_name, **validated_data)
        return branch