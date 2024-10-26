from datetime import timedelta

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from . import models, validation
from .services import HospitalService, AccountService


class TimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Timetable
        fields = ("id", "hospital_id", "doctor_id", "from", "to", "room")
        extra_kwargs = {
            "from": {
                "source": "from_date",
                "validators": [validation.time_every_30_minutes_only]
            },
            "to": {
                "validators": [validation.time_every_30_minutes_only]
            },
            "hospital_id": {
                "validators": [HospitalService().hospital_exists]
            },
            "doctor_id": {
                "validators": [AccountService().doctor_exists]
            }
        }
        validators = [validation.DeltaNoMoreThan(timedelta(hours=12))]

    def validate(self, attrs):
        if not HospitalService().hospital_room_exists(attrs["hospital_id"], attrs["room"]):
            raise ValidationError("No such room")
        return super().validate(attrs)


class AppointmentSerializer(serializers.ModelSerializer):
    timetable = TimetableSerializer()

    class Meta:
        model = models.Appointment
        fields = ("id", "pacient_id", "time", "timetable")
