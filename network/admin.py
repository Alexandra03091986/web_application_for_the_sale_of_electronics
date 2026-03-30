from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from network.models import Supplier, Contact, Product


@admin.action(description="Очистить задолженность перед поставщиком")
def clear_debt(modeladmin, request, queryset):
    queryset.update(debt=0)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    """Настройка отображения модели Supplier в админке"""
    list_display = ("name", "level", "supplier_link", "debt", "created_at")
    list_filter = ("contact__city", "contact__country", "level" )   # Двойное подчеркивание для связи
    actions = [clear_debt]
    search_fields = ("name", "contact__city")

    def supplier_link(self, obj):
        if obj.supplier:
            url = reverse('admin:network_supplier_change', args=[obj.supplier.id])
            return format_html('<a href="{}">{}</a>', url, obj.supplier.name)
        return '-'

    supplier_link.short_description = 'Поставщик'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('supplier', 'contact')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """Настройка отображения модели Contact в админке"""
    list_display = ("email", "country", "city", "street", "house_number")
    search_fields = ("email", "country", "city")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Настройка отображения модели Product в админке"""
    list_display = ("name", "model", "release_date")
    search_fields = ("name", "model")
    list_filter = ("release_date",)
