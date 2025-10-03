from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from apps.applications.models import SpecialistsRequired
from apps.applications.api_endpoints.SpecialistsRequiredUpdateDetail.serializers import SpecialistRequiredUpdateSerializer


class SpecialistRequiredDetailUpdateAPIView(RetrieveUpdateAPIView):
    '''
    GET /api/specialists-required/<id>/update/
    PUT /api/specialists-required/<id>/update/
    PATCH /api/specialists-required/<id>/update/
    '''
    serializer_class = SpecialistRequiredUpdateSerializer
    permission_classes = [IsAdminUser | IsAuthenticated] 
    queryset = SpecialistsRequired.objects.all()
    lookup_field = 'pk'


__all__ = [
    'SpecialistRequiredDetailUpdateAPIView'
]
