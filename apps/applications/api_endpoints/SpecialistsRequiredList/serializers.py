from rest_framework import serializers

from apps.applications.models import SpecialistsRequired
from apps.applications.api_endpoints.SpecialtyList.serializers import SpecialtyListSerializer


class SpecialistsRequiredListSerializer(serializers.ModelSerializer):
    specialty = SpecialtyListSerializer(read_only=True)
    required_sp_name = serializers.CharField(source='required_specialists.title', read_only=True)


    class Meta:
        model = SpecialistsRequired
        fields = [
            'id',
            'specialty',
            'required_specialists',
            'required_sp_name',
            'min_count'
        ]
