from __future__ import annotations

from typing import Any

from rest_framework import serializers

from .models import Favorite, RecentlyViewed


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Favorite
        fields = ("id", "user", "route", "guide", "created_at")
        read_only_fields = ("created_at",)

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        if bool(data.get("route")) == bool(data.get("guide")):
            raise serializers.ValidationError("Provide exactly one of `route` or `guide`.")
        return data


class RecentlyViewedSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = RecentlyViewed
        fields = ("id", "user", "item_type", "item_id", "created_at")
        read_only_fields = ("created_at",)
