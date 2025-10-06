from django.utils.translation import gettext as _

from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from apps.applications.models import Branch
from apps.applications.api_endpoints.BranchCreate.serializers import BranchCreateSerializer


class BranchCreateAPIView(CreateAPIView):
    """
    POST /api/applications/branch-create/
    Create a new branch

    Example request body:
    {
        "district_name_input": "Olmazor tumani",
        "branch_name" : "Olmazor tuman branch"
    }
    """
    serializer_class = BranchCreateSerializer
    permission_classes = [IsAdminUser | IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        branch = serializer.save()
        return Response(
            {
                "message": _("Filial muvaffaqiyatli qo'shildi."),
                "data": self.get_serializer(branch).data
            },
            status=status.HTTP_201_CREATED
        )
    
__all__ = [
    "BranchCreateAPIView"
]