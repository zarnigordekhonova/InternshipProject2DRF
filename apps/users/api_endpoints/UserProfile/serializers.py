from rest_framework import serializers

from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class GetProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "username",
            "phone_number",
            "email",
            "avatar",
        )
        