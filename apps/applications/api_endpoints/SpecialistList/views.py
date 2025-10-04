from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.applications.models import Specialist
from apps.applications.api_endpoints.SpecialistList.serializers import SpecialistListSerializer


class SpecialistListAPIView(ListAPIView):
    """
    GET /api/applications/specialist-list/
    
    List all specialists
    """
    queryset = Specialist.objects.all().order_by('title')
    serializer_class = SpecialistListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['title']


__all__ = [
    "SpecialistListAPIView"
]