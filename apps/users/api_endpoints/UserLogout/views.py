from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


class UserLogoutAPIView(APIView):
    """
    POST /api/users/user-logout/

    For Postman:
    Send your refresh token in order to logout of your account.

    Example request body:
    {
        "refresh": "refresh_token"
    }
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"error": "refresh token missing"}, status=400)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=204)
        except Exception:
            return Response({"error": "invalid token"}, status=400)

__all__ = [
    "UserLogoutAPIView"
]
