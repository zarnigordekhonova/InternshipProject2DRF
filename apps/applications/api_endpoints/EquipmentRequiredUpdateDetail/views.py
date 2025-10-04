from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView

from apps.applications.models import EquipmentRequiredItem
from apps.applications.api_endpoints.EquipmentRequiredUpdateDetail.serializers import EquipmentRequiredItemUpdateSerializer


class EquipmentRequiredItemRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    """
    Updating/Getting information of required equipment on specific ID.

    PUT /api/applications/update/{id}/equipment-required/
    PATCH /api/applications/update/{id}/equipment-required/
    Update an existing required equipment data

    GET /api/api/applications/update/{id}/branch/
    To get required equipment data in detail on specific ID
    """
    queryset = EquipmentRequiredItem.objects.all()
    serializer_class = EquipmentRequiredItemUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        pk = kwargs.get("pk")
        try:
            branch = EquipmentRequiredItem.objects.get(pk=pk)
        except EquipmentRequiredItem.DoesNotExist:
            return Response({
                "detail": "Bu id dagi minimal talab qilingan jihozlar ro'yxati topilmadi!"
                }, 
                status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(branch)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

__all__ = [
    'EquipmentRequiredItemRetrieveUpdateView'
]
