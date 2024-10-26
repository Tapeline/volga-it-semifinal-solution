from django.db import models


class Document(models.Model):
    date = models.DateTimeField()
    pacient_id = models.IntegerField()
    hospital_id = models.IntegerField()
    doctor_id = models.IntegerField()
    room = models.CharField()
    data = models.TextField()
