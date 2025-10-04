from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.applications.models import SpecialistsRequired
from apps.applications.api_endpoints.SpecialistsRequiredList.serializers import SpecialistsRequiredListSerializer


class SpecialistsRequiredListAPIView(ListAPIView):
    """
    GET /api/applications/specialist-required-list/
    
    Get a list of required specialists linked to specific specialties.
    """
    serializer_class = SpecialistsRequiredListSerializer
    permission_classes = [IsAuthenticated]
    queryset = SpecialistsRequired.objects.select_related('specialty', 'required_specialists')
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['specialty', 'required_specialists__title']
    ordering_fields = ['specialty', 'required_specialists__title']



__all__ = [
    "SpecialistsRequiredListAPIView"
]
