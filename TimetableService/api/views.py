import datetime

from django.http import HttpResponse
from drf_spectacular.utils import extend_schema, OpenApiResponse, extend_schema_view, OpenApiRequest, OpenApiParameter
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (CreateAPIView, GenericAPIView, DestroyAPIView)
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import permissions, serializers, models, swagger
from .exceptions import AppointmentAlreadyExistsException


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
        **swagger.created(serializers.TimetableSerializer),
        **swagger.forbidden(),
        **swagger.bad_request(),
        **swagger.not_authorized()
    })
)
class CreateTimetableView(CreateAPIView):
    """Create timetable (admin or manager only)"""
    permission_classes = (IsAuthenticated, permissions.HasAdminOrManagerRole)
    serializer_class = serializers.TimetableSerializer
    queryset = models.Timetable.objects.all()


@extend_schema_view(
    put=extend_schema(
        description="Update timetable (admin or manager only)",
        responses={
            **swagger.ok(
                serializers.TimetableSerializer,
                "Return updated timetable model"
            ),
            **swagger.bad_request(),
            **swagger.forbidden(),
            **swagger.not_authorized()
        }
    ),
    delete=extend_schema(
        description="Delete timetable (admin or manager only)",
        responses={
            **swagger.deleted(),
            **swagger.forbidden(),
            **swagger.not_authorized()
        }
    ),
)
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
        except BaseException:
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


@extend_schema_view(
    get=extend_schema(
        description="Get all timetables of provided doctor",
        parameters=[
            OpenApiParameter(
                name="from",
                description="From date",
                type=datetime.datetime,
                required=True
            ),
            OpenApiParameter(
                name="to",
                description="To date",
                type=datetime.datetime,
                required=True
            ),
        ],
        responses={
            **swagger.ok(
                serializers.TimetableSerializer,
                "Return all timetables of provided doctor"
            ),
            **swagger.not_authorized()
        }
    ),
    delete=extend_schema(
        description="Delete all timetables for doctor (admin or manager only)",
        responses={
            **swagger.deleted(),
            **swagger.forbidden(),
            **swagger.not_authorized()
        }
    ),
)
class RetrieveDeleteTimetablesByDoctorId(RetrieveDeleteTimetablesByParameterView):
    permission_classes = (IsAuthenticated, permissions.HasAdminOrManagerRoleOrReadOnly)

    def get_queryset(self):
        return super().get_queryset().filter(doctor_id=self.kwargs["doctor_id"])


@extend_schema_view(
    get=extend_schema(
        description="Get all timetables of provided hospital",
        parameters=[
            OpenApiParameter(
                name="from",
                description="From date",
                type=datetime.datetime,
                required=True
            ),
            OpenApiParameter(
                name="to",
                description="To date",
                type=datetime.datetime,
                required=True
            ),
        ],
        responses={
            **swagger.ok(
                serializers.TimetableSerializer,
                "Return all timetables of provided hospital"
            ),
            **swagger.not_authorized()
        }
    ),
    delete=extend_schema(
        description="Delete all timetables for hospital (admin or manager only)",
        responses={
            **swagger.deleted(),
            **swagger.forbidden(),
            **swagger.not_authorized()
        }
    ),
)
class RetrieveDeleteTimetablesByHospitalId(RetrieveDeleteTimetablesByParameterView):
    permission_classes = (IsAuthenticated, permissions.HasAdminOrManagerRoleOrReadOnly)

    def get_queryset(self):
        return super().get_queryset().filter(hospital_id=self.kwargs["hospital_id"])


@extend_schema_view(
    get=extend_schema(
        description="Get all timetables of provided hospital room",
        parameters=[
            OpenApiParameter(
                name="from",
                description="From date",
                type=datetime.datetime,
                required=True
            ),
            OpenApiParameter(
                name="to",
                description="To date",
                type=datetime.datetime,
                required=True
            ),
        ],
        responses={
            **swagger.ok(
                serializers.TimetableSerializer,
                "Return all timetables of provided hospital room"
            ),
            **swagger.not_authorized()
        }
    ),
    delete=extend_schema(
        description="Delete all timetables for hospital room (admin or manager only)",
        responses={
            **swagger.deleted(),
            **swagger.forbidden(),
            **swagger.not_authorized()
        }
    ),
)
class RetrieveDeleteTimetablesByRoomView(RetrieveDeleteTimetablesByParameterView):
    permission_classes = (IsAuthenticated, permissions.HasAdminOrManagerRoleOrReadOnly)

    def get_queryset(self):
        return super().get_queryset().filter(
            hospital_id=self.kwargs["hospital_id"],
            room=self.kwargs["room"]
        )


@extend_schema_view(
    get=extend_schema(
        description="Get all available slots in timetable",
        responses={
            **swagger.ok(
                {"type": "array", "items": {"type": "string", "format": "date-time"}},
                "Return all available slots in timetable"
            ),
            **swagger.not_authorized()
        }
    ),
    post=extend_schema(
        description="Create an appointment at selected time in timetable",
        request=OpenApiRequest({
            "type": "object",
            "properties": {
                "time": {
                    "type": "string",
                    "format": "date-time"
                }
            }
        }),
        responses={
            **swagger.created(serializers.AppointmentSerializer),
            **swagger.bad_request(),
            **swagger.conflict("Slot is already occupied"),
            **swagger.not_authorized()
        }
    ),
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
        target_time = datetime.datetime.fromisoformat(request.data["time"])
        if target_time < timetable.from_date or target_time > timetable.to:
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


@extend_schema_view(
    delete=extend_schema(
        description="Cancel appointment. It could be done only from the "
                    "account appointment was created for or admin/manager",
        responses={
            **swagger.deleted(),
            **swagger.forbidden(),
            **swagger.not_authorized()
        }
    ),
)
class DeleteAppointmentView(DestroyAPIView):
    permission_classes = (IsAuthenticated, permissions.CanDeleteThisAppointment)
    queryset = models.Appointment.objects.all()
