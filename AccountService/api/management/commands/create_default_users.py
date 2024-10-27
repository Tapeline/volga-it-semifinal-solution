from django.core.management import BaseCommand

from api import models


def _create_default_user_if_not_exists(username: str, role):
    if not models.User.objects.filter(username=username).exists():
        roles = {"User"}
        roles.add(role)
        models.User.objects.create_user(
            username=username,
            password=username,
            first_name=username.capitalize(),
            last_name=username.capitalize(),
            roles=list(roles)
        )


class Command(BaseCommand):
    def handle(self, *args, **options):
        _create_default_user_if_not_exists("admin", "Admin")
        _create_default_user_if_not_exists("manager", "Manager")
        _create_default_user_if_not_exists("doctor", "Doctor")
        _create_default_user_if_not_exists("user", "User")