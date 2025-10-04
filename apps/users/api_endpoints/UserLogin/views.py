from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import login

from apps.users.api_endpoints.UserLogin.serializers import UserLoginSerializer, UserSerializer

class UserLoginAPIView(GenericAPIView):
    """
    POST /api/users/user-login/
    Login in order to get refresh and access token.

    Example request body:
    {
        "phone_number": "+998991234567",
        "password": "example_password"
    }
    """
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        login(request, user)

        refresh = RefreshToken.for_user(user)

        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)
    


__all__ =[
    'UserLoginAPIView'
]