from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView

from apps.applications.models import Branch
from apps.applications.api_endpoints.BranchUpdateDetail.serializers import BranchUpdateSerializer


class BranchDetailUpdateAPIView(RetrieveUpdateAPIView):
    """
    Updating/Getting information of branch on specific ID.

    PUT /api/api/applications/update/{id}/branch/
    PATCH /api/api/applications/update/{id}/branch/
    Update an existing branch

    GET /api/api/applications/update/{id}/branch/
    To get an branch data in detail on specific ID
    """
    queryset = Branch.objects.all()
    serializer_class =  BranchUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            branch = Branch.objects.get(pk=pk)
        except Branch.DoesNotExist:
            return Response({"detail": "Bu id dagi filial topilmadi!"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(branch)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

__all__ = [
    "BranchDetailUpdateAPIView"
]