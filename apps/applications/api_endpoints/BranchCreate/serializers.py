from rest_framework import serializers
from apps.applications.models import Branch, District


class BranchCreateGetDistrictDataSerializer(serializers.ModelSerializer):
    class Meta:
        model =  District
        fields = ["district_name", "region"]


class BranchCreateSerializer(serializers.ModelSerializer):
    district = serializers.CharField(write_only=True)
    district_name = BranchCreateGetDistrictDataSerializer(read_only=True, source="district")
    region = serializers.CharField(read_only=True, source='district.region.region_name')
    
    class Meta:
        model = Branch
        fields = (
            "region",
            "district",  # tuman nomini kiritishda district field i bilan kiritiladi
            "district_name",  # ma'lumotni chiqarishda district_name field i bilan chiqadi
            "branch_name",
        )

    def create(self, validated_data):
        district = validated_data.pop("district")
        try: 
            district_name = District.objects.get(district_name=district)
        except District.DoesNotExist:
            raise serializers.ValidationError({"district": "Bunday nomdagi tuman mavjud emas."})
        except District.MultipleObjectsReturned:
            raise serializers.ValidationError({"district": "Bunday nomda bir nechta tuman mavjud, aniq nom kiriting."})
        
        branch = Branch.objects.create(district=district_name, **validated_data)
        return branch