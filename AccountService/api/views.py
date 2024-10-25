from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import (CreateAPIView, RetrieveAPIView,
                                     UpdateAPIView, ListAPIView,
                                     ListCreateAPIView, GenericAPIView)
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api import serializers, repo, permissions, pagination
from api.authentication import TokenWithInvalidation
from api.exceptions import UserAlreadyExistsException, BadRequestException, InvalidAccessTokenException


class UpdateDestroyAPIView(UpdateModelMixin, DestroyModelMixin,
                           GenericAPIView):
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class PingView(APIView):
    def get(self, request):
        return HttpResponse("ok", content_type="text/plain")


class RegisterView(CreateAPIView):
    serializer_class = serializers.RegistrationSerializer

    def create(self, request, *args, **kwargs):
        if repo.user_exists(request.data.get("username")):
            raise UserAlreadyExistsException
        return super().create(request, *args, **kwargs)


class LoginView(TokenObtainPairView):
    serializer_class = serializers.CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0]) from e

        repo.save_token(
            serializer.validated_data["user"],
            serializer.validated_data["access"],
            serializer.validated_data["refresh"]
        )
        return Response(
            {
                "access": serializer.validated_data["access"],
                "refresh": serializer.validated_data["refresh"]
            },
            status=status.HTTP_200_OK
        )


class LogOutView(APIView):
    permission_classes = (IsAuthenticated, )

    def put(self, request, *args, **kwargs):
        repo.invalidate_all_tokens_for_user(request.user)
        return Response(status=200)


class ValidateTokenView(APIView):
    def get(self, request, *args, **kwargs):
        access_token = request.query_params.get("access_token")
        if not isinstance(access_token, str):
            raise BadRequestException
        try:
            TokenWithInvalidation(access_token.encode())
        except TokenError:
            raise InvalidAccessTokenException
        return Response(status=status.HTTP_200_OK)


class RefreshTokenView(TokenRefreshView):
    serializer_class = serializers.CustomTokenRefreshSerializer


class ProfileView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user


class UpdateMyProfileView(UpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.UpdateMyProfileSerializer

    def get_object(self):
        return self.request.user


class ListCreateAllUsersView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, permissions.HasAdminRole)
    serializer_class = serializers.RegistrationFromAdminSerializer
    pagination_class = pagination.FromCountPagination
    queryset = repo.all_users()


class UpdateDestroyUserView(UpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, permissions.HasAdminRole)
    serializer_class = serializers.RegistrationFromAdminSerializer
    queryset = repo.all_users()

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.deleted = True
        repo.invalidate_all_tokens_for_user(user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListDoctorsView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.UserSerializer
    pagination_class = pagination.FromCountPagination
    queryset = repo.all_users(roles__contains="Doctor")

    def get_queryset(self):
        if not isinstance(self.request.query_params.get("name_filter"), str):
            return super().get_queryset()
        qs = super().get_queryset()
        id_list = [user.id for user in qs.all()
                   if self.request.query_params["name_filter"] in f"{user.first_name} {user.last_name}"]
        return qs.filter(id__in=id_list)


class RetrieveDoctorView(RetrieveAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.UserSerializer
    queryset = repo.all_users(roles__contains="Doctor")
