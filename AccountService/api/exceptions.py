from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework_simplejwt.exceptions import InvalidToken


class UserAlreadyExistsException(APIException):
    default_detail = "User with such name is already registered"
    default_code = "ALREADY_REGISTERED"
    status_code = status.HTTP_409_CONFLICT


class BadRequestException(APIException):
    default_detail = "Bad request format or data"
    default_code = "BAD_REQUEST"
    status_code = status.HTTP_400_BAD_REQUEST


class InvalidAccessTokenException(InvalidToken):
    default_detail = "Token invalidated"
    default_code = "TOKEN_INVALIDATED"


class InvalidRefreshTokenException(APIException):
    default_detail = "Refresh token invalidated"
    default_code = "TOKEN_INVALIDATED"
    status_code = status.HTTP_401_UNAUTHORIZED


class UserDeletedException(APIException):
    default_detail = "User deleted"
    default_code = "USER_DELETED"
    status_code = status.HTTP_404_NOT_FOUND
