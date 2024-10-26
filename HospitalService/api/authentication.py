import requests
from rest_framework import authentication

from hospital_service import settings


class User:
    def __init__(self, uid, username, first_name, last_name, roles):
        self.uid = uid
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.roles = roles
        self.is_authenticated = True


class RemoteAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        bearer_string: str = request.META.get('HTTP_AUTHORIZATION')
        if bearer_string is None:
            return None
        response = requests.get(
            f"{settings.ACCOUNT_SERVICE}/api/Accounts/Me/",
            headers={
                "Authorization": bearer_string
            }
        )
        if response.status_code == 200:
            data = response.json()
            return User(
                data["id"],
                data["username"],
                data["firstName"],
                data["lastName"],
                data["roles"]
            ), None
        return None
