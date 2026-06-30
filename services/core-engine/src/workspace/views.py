"""Travel workspace API — trips and their day-by-day items.

Everything is scoped to the logged-in tourist: you only ever see and edit your
own trips. Items support drag-and-drop reordering and a budget summary.
"""
from __future__ import annotations

from decimal import Decimal

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import TravelWorkspace, WorkspaceItem
from .serializers import (
    ReorderItemSerializer,
    TravelWorkspaceDetailSerializer,
    TravelWorkspaceSerializer,
    WorkspaceItemSerializer,
)


class TravelWorkspaceViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return (
            TravelWorkspace.objects.filter(tourist=self.request.user)
            .prefetch_related("items")
        )

    def get_serializer_class(self):
        if self.action == "retrieve":
            return TravelWorkspaceDetailSerializer
        return TravelWorkspaceSerializer

    def perform_create(self, serializer):
        serializer.save(tourist=self.request.user)

    @action(detail=True, methods=["get"], url_path="budget-summary")
    def budget_summary(self, request, *args, **kwargs):
        workspace = self.get_object()
        by_category: dict[str, float] = {}
        planned = Decimal("0.00")
        for item in workspace.items.all():
            by_category[item.item_type] = float(
                Decimal(str(by_category.get(item.item_type, 0))) + item.estimated_cost_npr
            )
            planned += item.estimated_cost_npr
        budget = workspace.total_budget_npr
        return Response(
            {
                "total_budget_npr": float(budget),
                "total_planned_npr": float(planned),
                "remaining_npr": float(budget - planned),
                "is_over_budget": planned > budget,
                "by_category": by_category,
            }
        )


class WorkspaceItemViewSet(viewsets.ModelViewSet):
    serializer_class = WorkspaceItemSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return WorkspaceItem.objects.filter(workspace__tourist=self.request.user).select_related(
            "route", "guide", "package"
        )

    @action(detail=False, methods=["post"], url_path="reorder")
    def reorder(self, request, *args, **kwargs):
        """Bulk drag-and-drop reorder. Body: [{item_id, day_number, display_order}, ...]."""
        payload = ReorderItemSerializer(data=request.data, many=True)
        payload.is_valid(raise_exception=True)

        owned = {i.id: i for i in self.get_queryset()}
        to_update = []
        for row in payload.validated_data:
            item = owned.get(row["item_id"])
            if item is None:
                continue
            item.day_number = row["day_number"]
            item.display_order = row["display_order"]
            to_update.append(item)
        if to_update:
            WorkspaceItem.objects.bulk_update(to_update, ["day_number", "display_order", "updated_at"])
        return Response(
            WorkspaceItemSerializer(self.get_queryset(), many=True).data,
            status=status.HTTP_200_OK,
        )
