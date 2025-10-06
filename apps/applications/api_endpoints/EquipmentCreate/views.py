from django.utils.translation import gettext as _

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from apps.applications.models import Equipment
from apps.applications.api_endpoints.EquipmentCreate.serializers import EquipmentCreateSerializer


class EquipmentCreateAPIView(CreateAPIView):
    """
    POST /api/applications/equipment-create/
    Add a new equipment name with its description.

    Example request body:
    {
        "name": "X-ray machine",
        "description": "description"
    }
    """
    serializer_class = EquipmentCreateSerializer
    permission_classes = [IsAdminUser | IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        branch = serializer.save()
        return Response(
            {
                "message": _("Jihoz nomi muvaffaqiyatli qo'shildi."),
                "data": self.get_serializer(branch).data
            },
            status=status.HTTP_201_CREATED
        )
    
__all__ = [
    "EquipmentCreateAPIView"
]