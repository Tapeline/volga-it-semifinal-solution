from rest_framework import serializers

from . import models


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Hospital
        fields = ("id", "name", "address", "contact_phone", "rooms")
