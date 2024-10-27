from django.http import HttpResponse
from drf_spectacular.utils import extend_schema, OpenApiResponse, extend_schema_view
from rest_framework import status
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import permissions, serializers, pagination, repo, swagger


class PingView(APIView):
    @extend_schema(responses={
        200: OpenApiResponse(description="Service alive")
    })
    def get(self, request):
        """Check if service is alive"""
        return HttpResponse("ok", content_type="text/plain")


@extend_schema_view(
    get=extend_schema(
        description="Get all hospitals",
        responses={
            **swagger.ok(
                serializers.HospitalSerializer,
                "Return all hospitals"
            ),
            **swagger.not_authorized()
        }
    ),
    post=extend_schema(
        description="Create a hospital (admin only)",
        responses={
            **swagger.created(serializers.HospitalSerializer),
            **swagger.bad_request(),
            **swagger.forbidden(),
            **swagger.not_authorized()
        }
    ),
)
class ListCreateHospitalView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, permissions.HasAdminRoleOrReadOnly)
    serializer_class = serializers.HospitalSerializer
    queryset = repo.all_hospitals()
    pagination_class = pagination.FromCountPagination


@extend_schema_view(
    get=extend_schema(
        description="Get hospital",
        responses={
            **swagger.ok(
                serializers.HospitalSerializer,
                "Return hospital data"
            ),
            **swagger.not_found(),
            **swagger.not_authorized()
        }
    ),
    put=extend_schema(
        description="Update hospital (admin only)",
        responses={
            **swagger.ok(
                serializers.HospitalSerializer,
                "Return updated hospital"
            ),
            **swagger.bad_request(),
            **swagger.forbidden(),
            **swagger.not_authorized()
        }
    ),
    delete=extend_schema(
        description="Soft delete hospital (admin only)",
        responses={
            **swagger.deleted(),
            **swagger.forbidden(),
            **swagger.not_authorized()
        }
    ),
)
class RetrieveUpdateDestroyHospitalView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, permissions.HasAdminRoleOrReadOnly)
    serializer_class = serializers.HospitalSerializer
    queryset = repo.all_hospitals()
    http_method_names = ("get", "put", "delete")

    def delete(self, request, *args, **kwargs):
        hospital = self.get_object()
        hospital.deleted = True
        hospital.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetHospitalRoomsView(APIView):
    """Get all rooms in provided hospital"""
    permission_classes = (IsAuthenticated,)

    @extend_schema(responses={
        **swagger.ok(
            {"type": "array", "items": {"type": "string"}},
            "List all rooms"
        ),
        **swagger.not_found(),
        **swagger.not_authorized()
    })
    def get(self, request, *args, **kwargs):
        hospital = repo.all_hospitals().get(id=kwargs["pk"])
        return Response(hospital.rooms)


class HospitalExistsView(APIView):
    """Check if such hospital exists"""
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
            "exists": repo.hospital_exists(kwargs["pk"])
        }, status=200)


class HospitalRoomExistsView(APIView):
    """Check if room in such hospital exists"""
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
            "exists": repo.hospital_room_exists(kwargs["pk"], kwargs["room"])
        }, status=200)
