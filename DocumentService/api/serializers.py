from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from . import models
from .services import HospitalService, AccountService


def assert_true(validator, message):
    def inner(*args, **kwargs):
        if not validator(*args, **kwargs):
            raise ValidationError(message)
    return inner


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Document
        fields = "__all__"
        extra_kwargs = {
            "hospital_id": {
                "validators": [assert_true(HospitalService().hospital_exists, "No such hospital")]
            },
            "doctor_id": {
                "validators": [assert_true(AccountService().doctor_exists, "No such doctor")]
            },
            "pacient_id": {
                "validators": [assert_true(AccountService().user_exists, "No such user")]
            }
        }

    def validate(self, attrs):
        if not HospitalService().hospital_room_exists(attrs["hospital_id"], attrs["room"]):
            raise ValidationError("No such room")
        return super().validate(attrs)
