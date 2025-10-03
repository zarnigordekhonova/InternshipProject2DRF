from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from apps.applications.models import Specialty


class SpecialtyDeleteAPIView(DestroyAPIView):
    queryset = Specialty.objects.all()
    permission_classes = [IsAdminUser | IsAuthenticated]


__all__ = [
    "SpecialtyDeleteAPIView"
]
