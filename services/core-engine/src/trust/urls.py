from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PriceCheckView, ScamReportViewSet

router = DefaultRouter()
router.register(r"scam-reports", ScamReportViewSet, basename="scamreport")

urlpatterns = [
    path("price-check/", PriceCheckView.as_view(), name="price-check"),
    path("", include(router.urls)),
]
