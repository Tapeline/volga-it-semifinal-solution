from . import models


def all_hospitals(*args, **kwargs):
    return models.Hospital.objects.filter(*args, deleted=False, **kwargs)


def hospital_exists(uid):
    return all_hospitals(id=uid).exists()


def hospital_room_exists(uid, room_name: str):
    return hospital_exists(uid) and room_name in all_hospitals().get(id=uid).rooms
