from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from apps.users.api_endpoints.UserProfile.serializers import GetProfileSerializer


class GetProfileAPIView(RetrieveUpdateAPIView):
    """
    Updating/Getting information of user's profile.

    PUT /api/users/user-profile/
    PATCH /api/users/user-profile/
    Update user's profile information.

    GET /api/users/user-profile/
    To get user's profie information.
    """
    serializer_class = GetProfileSerializer
    permission_classes = [IsAuthenticated, ]

    def get_object(self):
        return self.request.user
    


__all__ = [
    "GetProfileAPIView"
]