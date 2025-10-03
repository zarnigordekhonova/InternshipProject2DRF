from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView

from applications.models import EquipmentRequiredItem
from apps.applications.api_endpoints.EquipmentRequiredUpdateDetail.serializers import EquipmentRequiredItemUpdateSerializer


class EquipmentRequiredItemRetrieveUpdateAPIView(RetrieveUpdateAPIView):
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
