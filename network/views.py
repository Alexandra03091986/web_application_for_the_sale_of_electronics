from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from network.models import Supplier
from network.permissions import IsActiveEmployee
from network.serializers import SupplierCreateUpdateSerializer, SupplierSerializer, SupplierListSerializer


class SupplierViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Supplier.
    Поддерживает полный CRUD с разными сериализаторами для разных действий.
    """
    queryset = Supplier.objects.select_related('contact').prefetch_related('products').all()
    permission_classes = [IsActiveEmployee]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['contact__country', 'level']
    search_fields = ['name', 'contact__city']
    ordering_fields = ['name', 'level', 'debt', 'created_at']
    ordering = ['name']

    def get_serializer_class(self):
        """
        Возвращает разные сериализаторы в зависимости от действия
        """
        if self.action == 'list':
            return SupplierListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return SupplierCreateUpdateSerializer
        return SupplierSerializer
