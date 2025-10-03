from rest_framework.generics import ListAPIView
from rest_framework import filters

from apps.applications.models import Equipment
from apps.applications.api_endpoints.EquipmentList.serializers import EquipmentListSerializer


class EquipmentListAPIView(ListAPIView):
    """
    GET /api/equipment-list/
    List all equipments
    """
    queryset = Equipment.objects.all().order_by('name')
    serializer_class = EquipmentListSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']


__all__= [
    'EquipmentListAPIView'
]
