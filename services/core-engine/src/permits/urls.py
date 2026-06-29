from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TrekkingPermitViewSet

router = DefaultRouter()
router.register(r'trekking-permits', TrekkingPermitViewSet, basename='trekkingpermit')

urlpatterns = [path('', include(router.urls))]
