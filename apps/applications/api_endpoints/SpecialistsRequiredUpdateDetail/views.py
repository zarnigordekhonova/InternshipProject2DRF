from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from apps.applications.models import SpecialistsRequired
from apps.applications.api_endpoints.SpecialistsRequiredUpdateDetail.serializers import SpecialistRequiredUpdateSerializer


class SpecialistRequiredDetailUpdateAPIView(RetrieveUpdateAPIView):
    """
    Updating/Getting information of required specialist on specific ID.

    PUT /api/applications/update/{id}/specialists-required/
    PATCH /api/applications/update/{id}/specialists-required/
    Update an existing required specialist data

    GET /api/applications/update/{id}/specialists-required/
    To get required specialist data in detail on specific ID
    """
    serializer_class = SpecialistRequiredUpdateSerializer
    permission_classes = [IsAdminUser | IsAuthenticated] 
    queryset = SpecialistsRequired.objects.all()
    lookup_field = 'pk'


__all__ = [
    'SpecialistRequiredDetailUpdateAPIView'
]
