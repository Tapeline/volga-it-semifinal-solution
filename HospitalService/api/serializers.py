from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from . import models


@extend_schema_field({
    "type": "array",
    "items": {"type": "string"},
    "example": ["Room 1", "Room 2"]
})
class RoomListField(serializers.JSONField):
    pass


class HospitalSerializer(serializers.ModelSerializer):
    rooms = RoomListField()

    class Meta:
        model = models.Hospital
        fields = ("id", "name", "address", "contact_phone", "rooms")
