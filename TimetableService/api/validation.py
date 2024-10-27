import datetime

from rest_framework.exceptions import ValidationError


def time_every_30_minutes_only(t: datetime.datetime):
    if t.second != 0 or t.minute % 30 != 0:
        raise ValidationError("Time should be HH:00:00 or HH:30:00 only")


class DeltaNoMoreThan:
    def __init__(self, delta):
        self.delta = delta

    def __call__(self, attrs):
        if attrs["to"] - attrs["from_date"] > self.delta:
            raise ValidationError(f"Diff from-to should not be more than {self.delta}")


def assert_true(validator, message):
    def inner(*args, **kwargs):
        if not validator(*args, **kwargs):
            raise ValidationError(message)
    return inner
