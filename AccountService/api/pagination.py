from collections import OrderedDict

from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class FromCountPagination(LimitOffsetPagination):
    limit_query_param = "count"
    offset_query_param = "from"
    default_limit = 20

    def get_limit(self, request):
        return super().get_limit(request)

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ("count", self.count),
            ("results", data)
        ]))

    def get_paginated_response_schema(self, schema):
        return {
            'type': 'object',
            'properties': {
                'count': {
                    'type': 'integer',
                    'example': 123,
                },
                'results': schema,
            },
        }


