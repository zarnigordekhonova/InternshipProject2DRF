from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.applications.models import Specialty
from apps.applications.api_endpoints.SpecialtyList.serializers import SpecialtyListSerializer


class SpecialtyListAPIView(ListAPIView):
    """
    GET /api/applications/specialty-list/
    
    Get the list of all specialties
    """
    queryset = Specialty.objects.all().order_by('name')
    serializer_class = SpecialtyListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']


__all__= [
    'SpecialtyListAPIView'
]
