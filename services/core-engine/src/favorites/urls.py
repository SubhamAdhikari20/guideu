from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FavoriteViewSet, RecentlyViewedViewSet

router = DefaultRouter()
router.register(r"favorites", FavoriteViewSet, basename="favorite")
router.register(r"recently-viewed", RecentlyViewedViewSet, basename="recentlyviewed")

urlpatterns = [path("", include(router.urls))]
