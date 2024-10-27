from django.http import HttpResponse
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from . import permissions, serializers, models, elastic, swagger


class PingView(APIView):
    @extend_schema(responses={
        200: OpenApiResponse(description="Service alive")
    })
    def get(self, request):
        """Check if service is alive"""
        return HttpResponse("ok", content_type="text/plain")


class ListHistoryForUserView(ListAPIView):
    """
    Get all documents for provided patient.
    Only doctors and mentioned patient can access this page
    """
    permission_classes = (IsAuthenticated, permissions.IsDoctorOrThatPatient)
    serializer_class = serializers.DocumentSerializer
    queryset = models.Document.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(pacient_id=self.kwargs["pacient_id"])


@extend_schema_view(
    put=extend_schema(
        description="Update document and reindex it. "
                    "Only doctors and this patient can access this page",
        responses={
            **swagger.ok(
                serializers.DocumentSerializer,
                "Return updated document"
            ),
            **swagger.bad_request(),
            **swagger.forbidden(),
            **swagger.not_authorized()
        }
    ),
    get=extend_schema(
        description="Get document. "
                    "Only doctors and this patient can access this page",
        responses={
            **swagger.ok(
                serializers.DocumentSerializer,
                "Return document"
            ),
            **swagger.forbidden(),
            **swagger.not_authorized()
        }
    ),
)
class RetrieveUpdateDocumentView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, permissions.CanEditOrPatientReadOnly)
    serializer_class = serializers.DocumentSerializer
    queryset = models.Document.objects.all()
    http_method_names = ("get", "put")

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code != 200:
            return response
        elastic.update_document(response.data["id"], response.data)
        return response


@extend_schema_view(
    post=extend_schema(responses={
        **swagger.created(serializers.DocumentSerializer),
        **swagger.forbidden(),
        **swagger.bad_request(),
        **swagger.not_authorized()
    })
)
class CreateDocumentView(CreateAPIView):
    """Create document. Only admins, managers and doctors can create documents"""
    permission_classes = (IsAuthenticated, permissions.CanCreateDocument)
    serializer_class = serializers.DocumentSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code != 201:
            return response
        elastic.index_document(response.data["id"], response.data)
        return response
