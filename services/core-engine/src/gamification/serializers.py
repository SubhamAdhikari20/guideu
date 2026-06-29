from __future__ import annotations

from rest_framework import serializers

from .models import Badge, BadgeAward


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = ("id", "name", "category", "points", "trigger_event", "description", "is_active")


class BadgeAwardSerializer(serializers.ModelSerializer):
    badge_name = serializers.CharField(source="badge.name", read_only=True)
    category = serializers.CharField(source="badge.category", read_only=True)

    class Meta:
        model = BadgeAward
        fields = ("id", "user", "badge", "badge_name", "category", "points_awarded", "trigger_event", "created_at")
        read_only_fields = ("user", "points_awarded", "created_at")


class LeaderboardEntrySerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    total_points = serializers.IntegerField()
    badge_count = serializers.IntegerField()
