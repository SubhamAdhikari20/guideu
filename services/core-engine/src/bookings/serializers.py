from __future__ import annotations

from typing import Any

from rest_framework import serializers

from src.authentication.models import User
from .models import TourPackage, BookingSession, ItineraryItem


class TourPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TourPackage
        fields = ('id', 'title', 'description', 'base_price', 'duration_days', 'capacity', 'is_active', 'created_at')


class ItineraryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItineraryItem
        fields = ('id', 'day_index', 'title', 'description', 'location', 'start_time', 'end_time')


class BookingSessionSerializer(serializers.ModelSerializer):
    itinerary_items = ItineraryItemSerializer(many=True, read_only=True)
    # The tourist is taken from the logged-in user in the view, so clients never
    # send (or spoof) it.
    tourist = serializers.PrimaryKeyRelatedField(read_only=True)
    tour_package_title = serializers.CharField(source='tour_package.title', read_only=True)
    assigned_guide = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role=User.Roles.GUIDE), required=False, allow_null=True)

    class Meta:
        model = BookingSession
        fields = ('id', 'booking_reference', 'tourist', 'tour_package', 'tour_package_title', 'route', 'start_date', 'end_date', 'status', 'assigned_guide', 'total_price', 'notes', 'itinerary_items')
        read_only_fields = ('booking_reference', 'total_price')

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        start = data.get('start_date', getattr(self.instance, 'start_date', None))
        end = data.get('end_date', getattr(self.instance, 'end_date', None))
        if start and end and end <= start:
            raise serializers.ValidationError({'end_date': 'end_date must be after start_date'})
        guide = data.get('assigned_guide')
        if guide and not guide.is_guide_verified:
            raise serializers.ValidationError({'assigned_guide': 'Guide must be verified to be assigned to bookings.'})
        return data

    def create(self, validated_data: dict[str, Any]) -> BookingSession:
        # Compute total_price simply as base_price for now; complex pricing belongs to a service layer
        tour = validated_data['tour_package']
        validated_data['total_price'] = tour.base_price
        # Create a unique booking reference
        import uuid

        validated_data['booking_reference'] = uuid.uuid4().hex[:12].upper()
        return super().create(validated_data)
