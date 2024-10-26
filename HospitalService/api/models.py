from django.db import models


class Hospital(models.Model):
    name = models.CharField()
    address = models.CharField()
    contact_phone = models.CharField()
    rooms = models.JSONField()
    deleted = models.BooleanField(default=False)
