from django.utils.translation import gettext as _

from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView

from apps.applications.models import Equipment
from apps.applications.api_endpoints.EquipmentCreate.serializers import EquipmentCreateSerializer


class EquipmentUpdateDetailAPIView(RetrieveUpdateAPIView):
    """
    Updating/Getting information of equipment on specific ID.

    PUT /api/applications/update/{id}/equipment/
    PATCH /api/applications/update/{id}/equipment/
    Update an existing equipment data

    GET /api/applications/update/{id}/equipment/
    To get an equipment data in detail on specific ID
    """
    queryset = Equipment.objects.all()
    serializer_class =  EquipmentCreateSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            equipment = Equipment.objects.get(pk=pk)
        except Equipment.DoesNotExist:
            return Response({"detail": _("Bu id dagi jihoz nomi topilmadi!")}, 
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(equipment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

__all__ = [
    'EquipmentUpdateDetailAPIView'
]