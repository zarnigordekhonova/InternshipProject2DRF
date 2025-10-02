from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from django.contrib.auth import get_user_model

from apps.users.api_endpoints.UserRegister.serializers import UserRegisterSerializer

CustomUser = get_user_model()


class UserRegisterAPIView(CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            'user': self.get_serializer(user).data,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)


__all__ = [
    'UserRegisterAPIView'
]