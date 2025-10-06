from django.utils.translation import gettext as _

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView

from apps.applications.models import Specialty
from apps.applications.api_endpoints.SpecialtyCreate.serializers import SpecialtyCreateSerializer


class SpecialtyUpdateDetailAPIView(RetrieveUpdateAPIView):
    """
    Updating/Getting information of specialty on specific ID.

    PUT /api/applications/update/{id}/specialty/
    PATCH /api/applications/update/{id}/specialty/
    Update an existing specialty data

    GET /api/applications/update/{id}/specialty/
    To get an specialty data in detail on specific ID
    """
    queryset = Specialty.objects.all()
    serializer_class =  SpecialtyCreateSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            branch = Specialty.objects.get(pk=pk)
        except Specialty.DoesNotExist:
            return Response({"detail": _("Bu id dagi ixtisoslik topilmadi!")}, 
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(branch)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

__all__ = [
    'SpecialtyUpdateDetailAPIView'
]