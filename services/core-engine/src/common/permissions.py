"""Reusable, least-privilege DRF permissions.

Object-level checks default to a safe, owner-scoped policy so a viewset cannot
accidentally expose another user's data simply by forgetting to override
``get_queryset``.
"""
from __future__ import annotations

from typing import Any

from rest_framework import permissions
from rest_framework.request import Request


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Read for anyone authenticated; write only for the object's owner.

    The owner attribute name is configurable per-view via ``owner_field``
    (defaults to ``user``). Falls back to common owner field names.
    """

    owner_fields = ("user", "owner", "tourist", "applicant", "author")

    def _owner(self, view: Any, obj: Any):
        configured = getattr(view, "owner_field", None)
        candidates = (configured,) if configured else self.owner_fields
        for field in candidates:
            if field and hasattr(obj, field):
                return getattr(obj, field)
        return None

    def has_object_permission(self, request: Request, view: Any, obj: Any) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        if not (user and user.is_authenticated):
            return False
        if user.is_staff:
            return True
        return self._owner(view, obj) == user


class IsAdminOrReadOnly(permissions.BasePermission):
    """Anyone may read; only staff may write. For curated catalog content."""

    def has_permission(self, request: Request, view: Any) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class IsRole(permissions.BasePermission):
    """Permission factory keyed on the custom user ``role`` field.

    Usage::

        permission_classes = [IsRole.as_role("GUIDE", "ADMIN")]
    """

    required_roles: tuple[str, ...] = ()

    @classmethod
    def as_role(cls, *roles: str) -> type["IsRole"]:
        return type(f"IsRole_{'_'.join(roles)}", (cls,), {"required_roles": tuple(roles)})

    def has_permission(self, request: Request, view: Any) -> bool:
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and (user.is_staff or getattr(user, "role", None) in self.required_roles)
        )
