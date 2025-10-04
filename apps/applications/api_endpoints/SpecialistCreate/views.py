from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from apps.applications.models import Specialist
from apps.applications.api_endpoints.SpecialistCreate.serializers import SpecialistCreateSerializer


class SpecialistCreateAPIView(CreateAPIView):
    """
    POST /api/applications/specialist-create/
    Add a new specialist data

    Example request body:
    {
        "title": "Lor"
    }
    """
    serializer_class = SpecialistCreateSerializer
    permission_classes = [IsAdminUser | IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        branch = serializer.save()
        return Response(
            {
                "message": "Mutaxassis muvaffaqiyatli qo'shildi.",
                "data": self.get_serializer(branch).data
            },
            status=status.HTTP_201_CREATED
        )
    
__all__ = [
    "SpecialistCreateAPIView"
]