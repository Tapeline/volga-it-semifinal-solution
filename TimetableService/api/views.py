import datetime

from django.http import HttpResponse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (CreateAPIView, GenericAPIView, DestroyAPIView)
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import permissions, serializers, models
from .exceptions import AppointmentAlreadyExistsException


class UpdateDestroyAPIView(UpdateModelMixin, DestroyModelMixin,
                           GenericAPIView):
    http_method_names = ("delete", "put")

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class PingView(APIView):
    def get(self, request):
        return HttpResponse("ok", content_type="text/plain")


class CreateTimetableView(CreateAPIView):
    permission_classes = (IsAuthenticated, permissions.HasAdminOrManagerRole)
    serializer_class = serializers.TimetableSerializer
    queryset = models.Timetable.objects.all()


class UpdateDestroyTimetableView(UpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, permissions.HasAdminOrManagerRole)
    serializer_class = serializers.TimetableSerializer
    queryset = models.Timetable.objects.all()


class RetrieveDeleteTimetablesByParameterView(APIView):
    permission_classes = (IsAuthenticated, permissions.HasAdminOrManagerRoleOrReadOnly)

    def get_queryset(self):
        return models.Timetable.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            from_date = datetime.datetime.fromisoformat(request.GET.get("from"))
            to_date = datetime.datetime.fromisoformat(request.GET.get("to"))
        except TypeError | ValueError:
            raise ValidationError("from and to should be iso8601 strings")
        timetables = self.get_queryset().filter(
            from_date__gte=from_date,
            to__lte=to_date
        )
        return Response([
            serializers.TimetableSerializer(instance=t).data
            for t in timetables
        ])

    def delete(self, request, *args, **kwargs):
        self.get_queryset().delete()
        return Response(status=204)


class RetrieveDeleteTimetablesByDoctorId(RetrieveDeleteTimetablesByParameterView):
    permission_classes = (IsAuthenticated, permissions.HasAdminOrManagerRoleOrReadOnly)

    def get_queryset(self):
        return super().get_queryset().filter(doctor_id=self.kwargs["doctor_id"])


class RetrieveDeleteTimetablesByHospitalId(RetrieveDeleteTimetablesByParameterView):
    permission_classes = (IsAuthenticated, permissions.HasAdminOrManagerRoleOrReadOnly)

    def get_queryset(self):
        return super().get_queryset().filter(hospital_id=self.kwargs["hospital_id"])


class RetrieveDeleteTimetablesByRoomView(RetrieveDeleteTimetablesByParameterView):
    permission_classes = (IsAuthenticated, permissions.HasAdminOrManagerRoleOrReadOnly)

    def get_queryset(self):
        return super().get_queryset().filter(
            hospital_id=self.kwargs["hospital_id"],
            room=self.kwargs["room"]
        )


class AppointmentsView(APIView):
    parser_classes = (JSONParser, )

    def get(self, request, *args, **kwargs):
        timetable = models.Timetable.objects.get(id=kwargs["pk"])
        delta = datetime.timedelta(minutes=30)
        time = timetable.from_date
        slots = []
        while time <= timetable.to:
            slots.append(time)
            time += delta
        return Response([
            time.isoformat()
            for time in slots
            if not models.Appointment.objects.filter(timetable=timetable, time=time).exists()
        ])

    def post(self, request, *args, **kwargs):
        timetable = models.Timetable.objects.get(id=kwargs["pk"])
        target_time = request.data.time
        if target_time < timetable.from_date or timetable > timetable.to:
            raise ValidationError("time should be in timetable bounds")
        if models.Appointment.objects.filter(timetable=timetable, time=target_time).exists():
            raise AppointmentAlreadyExistsException
        obj = models.Appointment.objects.create(
            timetable=timetable, time=target_time, pacient_id=request.user.id
        )
        return Response(
            serializers.AppointmentSerializer(obj).data,
            status=status.HTTP_201_CREATED
        )


class DeleteAppointmentView(DestroyAPIView):
    permission_classes = (IsAuthenticated, permissions.CanDeleteThisAppointment)
    queryset = models.Appointment.objects.all()
