from typing import Any

from rest_framework import permissions

from .models import User


class IsVerifiedGuide(permissions.BasePermission):
    def has_permission(self, request: Any, view: Any) -> bool:
        user = getattr(request, 'user', None)
        return bool(user and user.is_authenticated and user.role == User.Roles.GUIDE and user.is_guide_verified)


class IsTouristOwner(permissions.BasePermission):
    def has_object_permission(self, request: Any, view: Any, obj: Any) -> bool:
        owner = getattr(obj, 'user', None)
        return bool(request.user and request.user.is_authenticated and owner == request.user)
