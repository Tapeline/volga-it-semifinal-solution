from django.http import HttpResponse
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from . import permissions, serializers, models, elastic


class PingView(APIView):
    def get(self, request):
        return HttpResponse("ok", content_type="text/plain")


class ListHistoryForUserView(ListAPIView):
    permission_classes = (IsAuthenticated, permissions.IsDoctorOrThatPatient)
    serializer_class = serializers.DocumentSerializer
    queryset = models.Document.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(pacient_id=self.kwargs["pacient_id"])


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


class CreateDocumentView(CreateAPIView):
    permission_classes = (IsAuthenticated, permissions.CanCreateDocument)
    serializer_class = serializers.DocumentSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code != 201:
            return response
        elastic.index_document(response.data["id"], response.data)
        return response

