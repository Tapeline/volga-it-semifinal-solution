from django.db import models


class Timetable(models.Model):
    hospital_id = models.IntegerField()
    doctor_id = models.IntegerField()
    from_date = models.DateTimeField()
    to = models.DateTimeField()
    room = models.CharField()


class Appointment(models.Model):
    timetable = models.ForeignKey(to=Timetable, on_delete=models.CASCADE)
    pacient_id = models.IntegerField()
    time = models.DateTimeField()
