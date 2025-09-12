from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.exceptions import ValidationError

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone', 'email', 'name', 'role', 'is_active']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'phone', 'email', 'name', 'role', 'password']

    def validate(self, attrs):
        phone = attrs.get('phone')
        email = attrs.get('email')

        # Normalize empty strings to None
        if phone == '':
            attrs['phone'] = None
        if email == '':
            attrs['email'] = None

        if not attrs.get('phone') and not attrs.get('email'):
            raise ValidationError("Either phone or email is required.")

        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom login serializer that accepts email or phone + password.
    """
    def validate(self, attrs):
        identifier = attrs.get("email") or attrs.get("username")
        password = attrs.get("password")

        if not identifier or not password:
            raise AuthenticationFailed("Email/Phone and password are required.")

        user = authenticate(username=identifier, password=password)

        if not user:
            raise AuthenticationFailed("Invalid credentials")

        self.user = user
        data = super().validate(attrs)

        # Add custom user data
        data['user'] = {
            "id": user.id,
            "email": user.email,
            "phone": user.phone,
            "name": user.name,
            "role": user.role,
        }
        return data
