from __future__ import annotations

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from src.common.mixins import AutoOwnerMixin, OwnedQuerySetMixin

from .models import Favorite, RecentlyViewed
from .serializers import FavoriteSerializer, RecentlyViewedSerializer


class FavoriteViewSet(OwnedQuerySetMixin, AutoOwnerMixin, viewsets.ModelViewSet):
    """A user's wishlist of saved routes and guides."""

    queryset = Favorite.objects.select_related("route", "guide")
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)
    owner_field = "user"
    filterset_fields = ("route", "guide")


class RecentlyViewedViewSet(OwnedQuerySetMixin, AutoOwnerMixin, viewsets.ModelViewSet):
    """A user's recently-viewed items (implicit recommender signal)."""

    queryset = RecentlyViewed.objects.all()
    serializer_class = RecentlyViewedSerializer
    permission_classes = (IsAuthenticated,)
    owner_field = "user"
    filterset_fields = ("item_type",)
    http_method_names = ["get", "post", "delete", "head", "options"]
