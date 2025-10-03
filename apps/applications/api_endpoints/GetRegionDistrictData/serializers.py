from rest_framework import serializers

from apps.applications.models import Region, District


class GetRegionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['region_name', ]


class GetDistrictDataSerializer(serializers.ModelSerializer):
    region = GetRegionDataSerializer(read_only=True)

    class Meta:
        model = District
        fields = ['region', 'district_name',]
