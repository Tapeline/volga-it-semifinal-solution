from django.http import HttpResponse
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from . import permissions, serializers, models


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


class CreateDocumentView(CreateAPIView):
    permission_classes = (IsAuthenticated, permissions.CanCreateDocument)
    serializer_class = serializers.DocumentSerializer
