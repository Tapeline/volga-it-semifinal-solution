from django.http import HttpResponse
from rest_framework import status
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import permissions, serializers, pagination, repo


class PingView(APIView):
    def get(self, request):
        return HttpResponse("ok", content_type="text/plain")


class ListCreateHospitalView(ListCreateAPIView):
    permission_classes = (IsAuthenticated, permissions.HasAdminRoleOrReadOnly)
    serializer_class = serializers.HospitalSerializer
    queryset = repo.all_hospitals()
    pagination_class = pagination.FromCountPagination


class RetrieveUpdateDestroyHospitalView(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, permissions.HasAdminRoleOrReadOnly)
    serializer_class = serializers.HospitalSerializer
    queryset = repo.all_hospitals()

    def delete(self, request, *args, **kwargs):
        hospital = self.get_object()
        hospital.deleted = True
        hospital.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GetHospitalRoomsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        hospital = repo.all_hospitals().get(id=kwargs["pk"])
        return Response(hospital.rooms)
