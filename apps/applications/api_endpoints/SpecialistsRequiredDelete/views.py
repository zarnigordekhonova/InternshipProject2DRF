from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from apps.applications.models import SpecialistsRequired


class SpecialistsRequiredDeleteAPIView(DestroyAPIView):
    """
    DELETE /api/applications/delete/{id}/specialists-required/

    Delete required specialist data on specific ID.
    """
    queryset = SpecialistsRequired.objects.all()
    permission_classes = [IsAdminUser | IsAuthenticated]


__all__ = [
    "SpecialistsRequiredDeleteAPIView"
]
