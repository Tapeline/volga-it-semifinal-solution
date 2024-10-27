from typing import Dict, Any

from drf_spectacular.utils import extend_schema_serializer, extend_schema_field
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from api import models, repo
from api.exceptions import InvalidRefreshTokenException, UserDeletedException


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["username", "password", "first_name", "last_name"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return models.User.objects.create_user(**validated_data)


@extend_schema_field({
    "type": "array",
    "items": {"type": "string"},
    "example": ["Admin", "User"]
})
class RoleListField(serializers.JSONField):
    pass


class UserSerializer(serializers.ModelSerializer):
    roles = RoleListField()

    class Meta:
        model = models.User
        fields = ("id", "username", "first_name", "last_name", "roles")


class UpdateMyProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)

    class Meta:
        model = models.User
        fields = ("id", "username", "password", "first_name", "last_name")

    def update(self, instance, validated_data):
        instance.first_name = validated_data["first_name"]
        instance.last_name = validated_data["last_name"]
        instance.set_password(validated_data["password"])
        instance.save()
        return instance


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    refresh = serializers.CharField(default="refresh token", read_only=True)
    access = serializers.CharField(default="access token", read_only=True)

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        data = super().validate(attrs)
        if self.user.deleted:
            raise UserDeletedException
        data["user"] = self.user
        return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    refresh_token = serializers.CharField(write_only=True)
    refresh = serializers.CharField(default="refresh token", read_only=True)
    access = serializers.CharField(default="access token", read_only=True)

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        if not repo.is_refresh_token_valid(attrs["refresh_token"]):
            raise InvalidRefreshTokenException
        attrs["refresh"] = attrs["refresh_token"]
        return super().validate(attrs)


class RegistrationFromAdminSerializer(serializers.ModelSerializer):
    roles = RoleListField()

    class Meta:
        model = models.User
        fields = ("id", "username", "password", "first_name", "last_name", "roles")
        extra_kwargs = {"password": {"write_only": True}, "id": {"read_only": True}}

    def create(self, validated_data):
        return models.User.objects.create_user(**validated_data)
