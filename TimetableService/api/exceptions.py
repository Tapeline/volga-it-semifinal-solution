from rest_framework import status
from rest_framework.exceptions import APIException


class AppointmentAlreadyExistsException(APIException):
    default_detail = "Appointment slot is occupied"
    default_code = "APPOINTMENT_OCCUPIED"
    status_code = status.HTTP_409_CONFLICT
