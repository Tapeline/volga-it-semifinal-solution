from drf_spectacular.utils import OpenApiResponse
from rest_framework import serializers


class GenericErrorSchema(serializers.Serializer):
    code = serializers.CharField()
    detail = serializers.CharField()


class ErrorResponse(OpenApiResponse):
    def __init__(self, message):
        super().__init__(GenericErrorSchema, description=message)


def bad_request(message="Bad request format"):
    return {400: OpenApiResponse(None, message)}


def not_authorized(message="Not authorized"):
    return {401: ErrorResponse(message)}


def forbidden(message="Not enough permissions"):
    return {403: ErrorResponse(message)}


def not_found(message="Resource with such parameters cannot be found"):
    return {404: OpenApiResponse(None, message)}


def conflict(message="Inputted data conflicts with data on server"):
    return {409: ErrorResponse(message)}


def created(schema, message="Created"):
    return {201: OpenApiResponse(schema, message)}


def ok(schema, message):
    return {200: OpenApiResponse(schema, message)}


def deleted(message="Resource deleted"):
    return {204: OpenApiResponse(None, message)}
