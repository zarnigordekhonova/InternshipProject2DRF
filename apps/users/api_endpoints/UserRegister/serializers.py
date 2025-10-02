from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

CustomUser = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
  
    class Meta:
        model =  CustomUser
        fields = (
            "username",
            "phone_number",
            "email",
            "password",
        )
        extra_kwargs = {"password" : {"write_only": True}}

    def create(self, validated_data):
        user =  CustomUser(
            username = validated_data["username"],
            phone_number = validated_data["phone_number"],
            email = validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
    
    def to_representation(self, instance):
        return { 
            "Username": instance.username,
            "Phone number": instance.phone_number,
        }
        