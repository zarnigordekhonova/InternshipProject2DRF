from rest_framework import serializers

from apps.applications.models import Branch


class BranchListSerializer(serializers.ModelSerializer):
    district_name = serializers.CharField(source='district.district_name', read_only=True)
    region_name = serializers.CharField(source='district.region.region_name', read_only=True)
    region_id = serializers.IntegerField(source='district.region.id', read_only=True)
    
    class Meta:
        model = Branch
        fields = ['branch_name', 'district', 'district_name', 'region_id', 'region_name']