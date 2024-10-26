from . import models


def all_hospitals(*args, **kwargs):
    return models.Hospital.objects.filter(*args, deleted=False, **kwargs)
