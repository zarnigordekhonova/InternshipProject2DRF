from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from apps.applications.models import EquipmentRequiredItem


class EquipmentRequiredItemDestroyAPIView(DestroyAPIView):
    queryset = EquipmentRequiredItem.objects.all()
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except EquipmentRequiredItem.DoesNotExist:
            return Response(
                {"detail": "Bu id dagi minimal talab qilingan jihoz topilmadi!"},
                status=status.HTTP_404_NOT_FOUND
            )

        self.perform_destroy(instance)
        return Response(
            {"detail": "Jihoz muvaffaqiyatli o'chirildi."},
            status=status.HTTP_204_NO_CONTENT
        )


__all__ = [
    'EquipmentRequiredItemDestroyAPIView'
]