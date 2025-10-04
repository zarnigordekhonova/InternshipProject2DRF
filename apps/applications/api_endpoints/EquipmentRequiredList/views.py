from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.applications.models import EquipmentRequiredItem
from apps.applications.api_endpoints.EquipmentRequiredList.serializers import EquipmentRequiredItemListSerializer


class EquipmentRequiredItemListAPIView(ListAPIView):
    """
    GET /api/applications/equipment-required-list/
    
    Get a list of required equipments linked to specific specialties.
    """
    serializer_class = EquipmentRequiredItemListSerializer
    permission_classes = [IsAuthenticated]
    queryset = EquipmentRequiredItem.objects.select_related('equipment_required', 'equipment')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['equipment_required__specialty__name', 'equipment__name']
    ordering_fields = ['equipment_required__specialty__name', 'equipment__name']



__all__ = [
    "EquipmentRequiredItemListAPIView"
]
