from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from apps.applications.models import Equipment


class EquipmentDeleteAPIView(DestroyAPIView):
    """
    DELETE /api/applications/delete/{id}/equipment/

    Delete equipment data on specific ID.
    """
    queryset = Equipment.objects.all()
    permission_classes = [IsAdminUser | IsAuthenticated]



__all__ = [
    "EquipmentDeleteAPIView"
]