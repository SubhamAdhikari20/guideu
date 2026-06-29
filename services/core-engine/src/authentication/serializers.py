from __future__ import annotations

from typing import Any

from django.db import transaction
from rest_framework import serializers

from .models import GuideProfile, Language, TouristProfile, User


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('id', 'name')


class GuideProfileSerializer(serializers.ModelSerializer):
    languages = LanguageSerializer(many=True, read_only=True)

    class Meta:
        model = GuideProfile
        fields = ('id', 'user', 'license_number', 'verification_documents', 'bio', 'languages', 'service_areas', 'created_at', 'updated_at')
        read_only_fields = ('user', 'created_at', 'updated_at')


class TouristProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TouristProfile
        fields = ('id', 'user', 'emergency_contact_name', 'emergency_contact_phone', 'citizenship_document', 'passport_expiry_date', 'created_at', 'updated_at')
        read_only_fields = ('user', 'created_at', 'updated_at')


class UserSerializer(serializers.ModelSerializer):
    guide_profile = GuideProfileSerializer(read_only=True)
    tourist_profile = TouristProfileSerializer(read_only=True)
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'password', 'first_name', 'last_name', 'role', 'phone_number',
            'nationality', 'passport_number', 'citizenship_number', 'date_of_birth', 'is_guide_verified',
            'guide_profile', 'tourist_profile', 'created_at', 'updated_at'
        )
        read_only_fields = ('created_at', 'updated_at')

    def validate_email(self, value: str) -> str:
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return value

    @transaction.atomic
    def create(self, validated_data: dict[str, Any]) -> User:
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance: User, validated_data: dict[str, Any]) -> User:
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
