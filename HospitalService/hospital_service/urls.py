from django.urls import path, include
from drf_spectacular.views import (SpectacularAPIView,
                                   SpectacularSwaggerView)

urlpatterns = [
    path('api-schema/',
         SpectacularAPIView.as_view(), name='schema'),
    path('ui-swagger/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('api/', include("api.urls")),
]
