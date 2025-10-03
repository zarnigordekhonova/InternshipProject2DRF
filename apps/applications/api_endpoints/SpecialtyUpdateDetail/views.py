from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView

from apps.applications.models import Specialty
from apps.applications.api_endpoints.SpecialtyCreate.serializers import SpecialtyCreateSerializer


class SpecialtyUpdateDetailAPIView(RetrieveUpdateAPIView):
    queryset = Specialty.objects.all()
    serializer_class =  SpecialtyCreateSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            branch = Specialty.objects.get(pk=pk)
        except Specialty.DoesNotExist:
            return Response({"detail": "Bu id dagi ixtisoslik topilmadi!"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(branch)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

__all__ = [
    'SpecialtyUpdateDetailAPIView'
]