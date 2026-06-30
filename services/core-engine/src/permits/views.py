from __future__ import annotations

from rest_framework import permissions, viewsets

from .models import TrekkingPermit
from .serializers import TrekkingPermitSerializer


class TrekkingPermitViewSet(viewsets.ModelViewSet):
    queryset = TrekkingPermit.objects.all().order_by('-created_at')
    serializer_class = TrekkingPermitSerializer
    permission_classes = (permissions.IsAuthenticated,)
