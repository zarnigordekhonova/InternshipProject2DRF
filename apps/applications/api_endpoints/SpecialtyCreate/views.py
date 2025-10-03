from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from apps.applications.models import Specialty
from apps.applications.api_endpoints.SpecialtyCreate.serializers import SpecialtyCreateSerializer


class SpecialtyCreateAPIView(CreateAPIView):
    serializer_class = SpecialtyCreateSerializer
    permission_classes = [IsAdminUser | IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        branch = serializer.save()
        return Response(
            {
                "message": "Ixtisoslik muvaffaqiyatli qo'shildi.",
                "data": self.get_serializer(branch).data
            },
            status=status.HTTP_201_CREATED
        )
    
__all__ = [
    "SpecialtyCreateAPIView"
]