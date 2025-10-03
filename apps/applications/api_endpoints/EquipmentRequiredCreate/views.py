from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.applications.models import EquipmentRequiredItem
from apps.applications.api_endpoints.EquipmentRequiredCreate.serializers import (
    EquipmentRequiredItemCreateSerializer,
    EquipmentRequiredItemDetailSerializer)


class EquipmentRequiredItemCreateAPIView(CreateAPIView):
    # Example request body for entering more than one object
    """
        [
        {
            "specialty": "Cardiology",
            "equipment_name": "ECG Machine",
            "min_count": 2
        },
        {
            "specialty": "Cardiology",
            "equipment_name": "X-Ray Machine",
            "min_count": 1
        }
        ]

    """

    queryset = EquipmentRequiredItem.objects.all()
    serializer_class = EquipmentRequiredItemCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        is_many = isinstance(request.data, list)

        serializer = self.get_serializer(data=request.data, many=is_many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        if is_many:
            output_serializer = EquipmentRequiredItemDetailSerializer(serializer.instance, many=True)
        else:
            output_serializer = EquipmentRequiredItemDetailSerializer(serializer.instance)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


__all__ = [
    'EquipmentRequiredItemCreateAPIView'
] 


