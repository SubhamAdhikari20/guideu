from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BadgeAwardViewSet, BadgeViewSet

router = DefaultRouter()
router.register(r"badges", BadgeViewSet, basename="badge")
router.register(r"awards", BadgeAwardViewSet, basename="badgeaward")

urlpatterns = [path("", include(router.urls))]
