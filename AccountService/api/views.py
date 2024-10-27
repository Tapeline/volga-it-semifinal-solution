from django.http import HttpResponse
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiParameter, OpenApiResponse
from rest_framework import status
from rest_framework.generics import (CreateAPIView, RetrieveAPIView,
                                     UpdateAPIView, ListAPIView,
                                     ListCreateAPIView, GenericAPIView)
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api import serializers, repo, permissions, pagination, swagger
from api.authentication import TokenWithInvalidation
from api.exceptions import UserAlreadyExistsException, BadRequestException, InvalidAccessTokenException


class UpdateDestroyAPIView(UpdateModelMixin, DestroyModelMixin,
                           GenericAPIView):
    http_method_names = ("delete", "put")

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class PingView(APIView):
    @extend_schema(responses={
        200: OpenApiResponse(description="Service alive")
    })
    def get(self, request):
        """Check if service is alive"""
        return HttpResponse("ok", content_type="text/plain")


@extend_schema_view(
    post=extend_schema(responses={
        **swagger.created(serializers.RegistrationSerializer),
        **swagger.bad_request()
    })
)
class RegisterView(CreateAPIView):
    serializer_class = serializers.RegistrationSerializer

    def create(self, request, *args, **kwargs):
        """Register a user"""
        if repo.user_exists(request.data.get("username")):
            raise UserAlreadyExistsException
        return super().create(request, *args, **kwargs)


@extend_schema_view(
    post=extend_schema(responses={
        **swagger.ok(
            serializers.CustomTokenObtainPairSerializer,
            "Login successful"
        ),
        **swagger.not_authorized(),
        **swagger.bad_request()
    })
)
class LoginView(TokenObtainPairView):
    serializer_class = serializers.CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs) -> Response:
        """Login with password and obtain a token"""
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


@extend_schema_view(
    post=extend_schema(responses={
        **swagger.ok(None, "Logout successful"),
        **swagger.not_authorized()
    })
)
class LogOutView(APIView):
    permission_classes = (IsAuthenticated, )

    def put(self, request, *args, **kwargs):
        """Invalidate all user tokens"""
        repo.invalidate_all_tokens_for_user(request.user)
        return Response(status=200)


@extend_schema_view(
    get=extend_schema(
        responses={
            **swagger.ok(None, "Authorized"),
            **swagger.bad_request(),
            **swagger.not_authorized()
        },
        parameters=[
            OpenApiParameter(
                name="accessToken",
                description="Access token to check",
                type=str,
                required=True
            ),
        ]
    )
)
class ValidateTokenView(APIView):
    def get(self, request, *args, **kwargs):
        """Check if provided token is eligible for login (return 200 or 401)"""
        access_token = request.query_params.get("access_token")
        if not isinstance(access_token, str):
            raise BadRequestException
        try:
            TokenWithInvalidation(access_token.encode())
        except TokenError:
            raise InvalidAccessTokenException
        return Response(status=status.HTTP_200_OK)


@extend_schema_view(
    post=extend_schema(responses={
        **swagger.ok(
            serializers.CustomTokenRefreshSerializer,
            "Return new pair of tokens"
        ),
        **swagger.bad_request(),
        **swagger.not_authorized()
    })
)
class RefreshTokenView(TokenRefreshView):
    """Get a new pair of tokens by providing refresh token"""
    serializer_class = serializers.CustomTokenRefreshSerializer


@extend_schema_view(
    post=extend_schema(responses={
        **swagger.ok(
            serializers.UserSerializer,
            "Return profile"
        ),
        **swagger.not_authorized()
    })
)
class ProfileView(RetrieveAPIView):
    """View own profile"""
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user


@extend_schema_view(
    post=extend_schema(responses={
        **swagger.ok(
            serializers.UpdateMyProfileSerializer,
            "Return updated user model"
        ),
        **swagger.bad_request(),
        **swagger.not_authorized()
    })
)
class UpdateMyProfileView(UpdateAPIView):
    """Update own profile"""
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.UpdateMyProfileSerializer
    http_method_names = ("put",)

    def get_object(self):
        return self.request.user


@extend_schema_view(
    get=extend_schema(
        description="Get all users (admin only)",
        responses={
            **swagger.ok(
                serializers.RegistrationFromAdminSerializer,
                "Return all users"
            ),
            **swagger.forbidden(),
            **swagger.not_authorized()
        }
    ),
    post=extend_schema(
        description="Create a user with specific roles (admin only)",
        responses={
            **swagger.ok(
                serializers.RegistrationFromAdminSerializer,
                "Return updated user model"
            ),
            **swagger.bad_request(),
            **swagger.forbidden(),
            **swagger.not_authorized()
        }
    ),
)
class ListCreateAllUsersView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, permissions.HasAdminRole)
    serializer_class = serializers.RegistrationFromAdminSerializer
    pagination_class = pagination.FromCountPagination
    queryset = repo.all_users()


@extend_schema_view(
    put=extend_schema(
        description="Update user and his roles (admin only)",
        responses={
            **swagger.ok(
                serializers.RegistrationFromAdminSerializer,
                "Return updated user model"
            ),
            **swagger.bad_request(),
            **swagger.forbidden(),
            **swagger.not_authorized()
        }
    ),
    delete=extend_schema(
        description="Soft delete user (admin only)",
        responses={
            **swagger.deleted(),
            **swagger.forbidden(),
            **swagger.not_authorized()
        }
    ),
)
class UpdateDestroyUserView(UpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, permissions.HasAdminRole)
    serializer_class = serializers.RegistrationFromAdminSerializer
    queryset = repo.all_users()

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.deleted = True
        repo.invalidate_all_tokens_for_user(user)
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(
    get=extend_schema(
        parameters=[
            OpenApiParameter(
                name="nameFilter",
                description="Search doctor by name. Match happens if "
                            "doctor's full name (first + last name) "
                            "matches SQL LIKE %{nameFilter}%. In other words, "
                            "if firstName + ' ' + lastName contains nameFilter",
                type=str,
            ),
        ],
        responses={
            **swagger.ok(
                serializers.UserSerializer,
                "Return filtered doctors"
            ),
            **swagger.bad_request(),
            **swagger.not_authorized()
        }
    )
)
class ListDoctorsView(ListAPIView):
    """Get all users with Doctor role filtered by name"""
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


@extend_schema_view(
    get=extend_schema(
        responses={
            **swagger.ok(
                serializers.UserSerializer,
                "Return found doctor"
            ),
            **swagger.not_found(),
            **swagger.bad_request(),
            **swagger.not_authorized()
        }
    )
)
class RetrieveDoctorView(RetrieveAPIView):
    """Get a doctor profile"""
    permission_classes = (IsAuthenticated, )
    serializer_class = serializers.UserSerializer
    queryset = repo.all_users(roles__contains="Doctor")


class UserExistsView(APIView):
    """Check if user with that role exists"""

    @extend_schema(
        responses={
            **swagger.ok(
                {"type": "object", "properties": {"exists": {"type": "boolean"}}},
                "Return answer"
            )
        }
    )
    def get(self, request, *args, **kwargs):
        return Response({
            "exists": repo.user_with_role_exists(kwargs["pk"], kwargs["role"])
        }, status=200)
