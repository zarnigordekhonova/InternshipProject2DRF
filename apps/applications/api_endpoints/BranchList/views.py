from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from apps.applications.models import Branch
from apps.applications.api_endpoints.BranchList.serializers import BranchListSerializer


class BranchListAPIView(ListAPIView):
    serializer_class = BranchListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['district']
    search_fields = ['branch_name', 'district__district_name', 'district__region__region_name']
    ordering_fields = ['branch_name', 'district__district_name']
    
    def get_queryset(self):
        queryset = Branch.objects.select_related('district__region').order_by('district__region__region_name', 'district__district_name', 'branch_name')
        
        district_id = self.request.query_params.get('district', None)
        if district_id:
            queryset = queryset.filter(district_id=district_id)
        
        region_id = self.request.query_params.get('region', None)
        if region_id:
            queryset = queryset.filter(district__region_id=region_id)
        
        return queryset
    

__all__ = [
    "BranchListAPIView"
]
