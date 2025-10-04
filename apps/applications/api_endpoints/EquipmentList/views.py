from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.applications.models import Equipment
from apps.applications.api_endpoints.EquipmentList.serializers import EquipmentListSerializer


class EquipmentListAPIView(ListAPIView):
    """
    GET /api/applications/equipment-list/
    
    Get a list of all branchs with region and district data.
    """
    queryset = Equipment.objects.all().order_by('name')
    serializer_class = EquipmentListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']


__all__= [
    'EquipmentListAPIView'
]
