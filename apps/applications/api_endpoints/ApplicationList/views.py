from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.applications.models import Application
from apps.applications.api_endpoints.ApplicationList.serializers import ApplicationListSerializer

class ApplicationListAPIView(ListAPIView):
    """
    GET /api/applications/
    GET /api/applications/?status=DRAFT
    GET /api/applications/?status=SUBMITTED
    GET /api/applications/?search=john
    List all applications with filtering and search
    """
    serializer_class = ApplicationListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'document_type']
    search_fields = ['first_name', 'last_name', 'email', 'phone_number', 'registration_number']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = Application.objects.select_related('user').prefetch_related(
            'applicationbranch_set__branch__district__region',
            'applicationbranch_set__specialties',
            'applicationbranch_set__selected_specialists',
            'applicationbranch_set__selected_equipment'
        )
        
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        
        return queryset


__all__ = [
    'ApplicationListAPIView'
]