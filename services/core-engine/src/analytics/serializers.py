from __future__ import annotations

from rest_framework import serializers

from .models import UserEvent


class UserEventSerializer(serializers.ModelSerializer):
    actor = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = UserEvent
        fields = (
            "id", "actor", "event_type", "item_type", "item_id",
            "session_id", "source", "device", "metadata", "created_at",
        )
        read_only_fields = ("actor", "created_at")


class FunnelSerializer(serializers.Serializer):
    """Free-form mapping of event_type -> count."""

    def to_representation(self, instance):
        return instance
