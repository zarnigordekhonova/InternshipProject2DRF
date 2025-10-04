from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView

from apps.applications.models import Specialist
from apps.applications.api_endpoints.SpecialistCreate.serializers import SpecialistCreateSerializer


class SpecialistUpdateDetailAPIView(RetrieveUpdateAPIView):
    """
    Updating/Getting information of specialist on specific ID.

    PUT /api/applications/update/{id}/specialist/
    PATCH /api/applications/update/{id}/specialist/
    Update an existing specialist data

    GET /api/applications/update/{id}/specialist/
    To get an specialist data in detail on specific ID
    
    """
    queryset = Specialist.objects.all()
    serializer_class =  SpecialistCreateSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            branch = Specialist.objects.get(pk=pk)
        except Specialist.DoesNotExist:
            return Response({"detail": "Bu id dagi mutaxassis turi topilmadi!"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(branch)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

__all__ = [
    'SpecialistUpdateDetailAPIView'
]