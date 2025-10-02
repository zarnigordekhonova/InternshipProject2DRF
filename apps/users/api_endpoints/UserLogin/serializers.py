from rest_framework import serializers

from django.contrib.auth import get_user_model, authenticate

CustomUser = get_user_model()


class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        if phone_number and password:
            user = authenticate(request=self.context.get('request'),
                                phone_number=phone_number, password=password)
            if not user:
                raise serializers.ValidationError('Invalid email or password.')

            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError('You must write "phone_number" and "password".')
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            )