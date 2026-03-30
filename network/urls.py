from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .apps import NetworkConfig
from .views import SupplierViewSet

app_name = NetworkConfig.name

router = DefaultRouter()
router.register(r'suppliers', SupplierViewSet, basename='supplier')

urlpatterns = [
    path('', include(router.urls)),
]
