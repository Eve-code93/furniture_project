from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Allows login with either phone or email + password.
    """

    def validate(self, attrs):
        identifier = attrs.get("username")  # SimpleJWT expects "username" by default
        password = attrs.get("password")

        user = None
        if "@" in identifier:  # looks like email
            try:
                user_obj = User.objects.get(email=identifier)
                user = authenticate(email=user_obj.email, password=password)
            except User.DoesNotExist:
                pass
        else:  # assume phone
            try:
                user_obj = User.objects.get(phone=identifier)
                user = authenticate(phone=user_obj.phone, password=password)
            except User.DoesNotExist:
                pass

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        refresh = self.get_token(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserSerializer(user).data
        }
