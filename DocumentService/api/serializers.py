from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from . import models
from .services import HospitalService, AccountService


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Document
        fields = "__all__"
        extra_kwargs = {
            "hospital_id": {
                "validators": [HospitalService().hospital_exists]
            },
            "doctor_id": {
                "validators": [AccountService().doctor_exists]
            },
            "pacient_id": {
                "validators": [AccountService().user_exists]
            }
        }

    def validate(self, attrs):
        if not HospitalService().hospital_room_exists(attrs["hospital_id"], attrs["room"]):
            raise ValidationError("No such room")
        return super().validate(attrs)
