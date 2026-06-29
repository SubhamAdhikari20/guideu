from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserEventViewSet

router = DefaultRouter()
router.register(r"events", UserEventViewSet, basename="userevent")

urlpatterns = [path("", include(router.urls))]
