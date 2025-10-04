from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from apps.applications.models import Branch


class BranchDeleteAPIView(DestroyAPIView):
    """
    DELETE /api/applications/delete/{id}/branch/
    
    Delete a branch data on a specific ID.
    """
    queryset = Branch.objects.all()
    permission_classes = [IsAdminUser | IsAuthenticated]


__all__ = [
    "BranchDeleteAPIView"
]
