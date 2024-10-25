from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

schema_view = get_schema_view(
    openapi.Info(
        title="Account service API",
        default_version="v1",
        license=openapi.License(name="GNU GPL v3.0"),
    ),
    patterns=[path('api/', include("api.urls"))],
    public=True,
    permission_classes=[AllowAny],
    authentication_classes=(JWTAuthentication,)
)

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path("ui-swagger/", schema_view.with_ui('swagger', cache_timeout=0)),
    path('api/', include("api.urls")),
]
