from __future__ import annotations

from typing import Any

from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

# Canonical base models now live in ``common``. Re-exported here so existing
# imports (`from src.authentication.models import TimeStampedModel`) keep working.
from src.common.models import TimeStampedModel  # noqa: F401


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username: str, email: str, password: str | None, **extra_fields: Any):
        if not email:
            raise ValueError('The email must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username: str, email: str | None = None, password: str | None = None, **extra_fields: Any):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username: str, email: str | None = None, password: str | None = None, **extra_fields: Any):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser, TimeStampedModel):
    class Roles(models.TextChoices):
        TOURIST = 'TOURIST', 'Tourist'
        GUIDE = 'GUIDE', 'Guide'
        ADMIN = 'ADMIN', 'Administrator'

    email = models.EmailField(unique=True, db_index=True)
    role = models.CharField(max_length=16, choices=Roles.choices, default=Roles.TOURIST, db_index=True)
    phone_number = models.CharField(max_length=32, blank=True, null=True)
    nationality = models.CharField(max_length=64, blank=True, null=True)
    passport_number = models.CharField(max_length=64, blank=True, null=True, db_index=True)
    citizenship_number = models.CharField(max_length=64, blank=True, null=True, db_index=True)
    date_of_birth = models.DateField(blank=True, null=True)
    is_guide_verified = models.BooleanField(default=False, db_index=True)

    objects = UserManager()

    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class Language(TimeStampedModel):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        ordering = ['name']


class GuideProfile(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='guide_profile', db_index=True)
    license_number = models.CharField(max_length=128, blank=True, null=True)
    verification_documents = models.JSONField(blank=True, null=True)
    bio = models.TextField(blank=True)
    languages = models.ManyToManyField('authentication.Language', blank=True, related_name='guides')
    service_areas = models.JSONField(blank=True, null=True)


class TouristProfile(TimeStampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tourist_profile', db_index=True)
    emergency_contact_name = models.CharField(max_length=128, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=32, blank=True, null=True)
    citizenship_document = models.JSONField(blank=True, null=True)
    passport_expiry_date = models.DateField(blank=True, null=True)
