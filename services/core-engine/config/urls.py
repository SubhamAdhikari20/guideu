"""Root URL configuration.

All REST endpoints are versioned under ``/api/<version>/`` (URLPathVersioning,
``v1`` only for now). OpenAPI schema + Swagger UI are served via drf-spectacular.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from . import views

# Versioned API surface. The leading ``api/<version>/`` prefix supplies the
# ``version`` kwarg that DRF's URLPathVersioning reads.
# Sprint 1 exposes only the authentication surface. Domain routers
# (catalog, bookings, payments, reviews, …) are mounted here in later sprints.
api_patterns = [
    path("auth/", include("src.authentication.urls")),
]

urlpatterns = [
    path("", views.service_index, name="service-index"),
    path("healthz/", views.healthz, name="healthz"),
    path("admin/", admin.site.urls),
    # OpenAPI
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    # Versioned REST API
    path("api/<version>/", include(api_patterns)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
