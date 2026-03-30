from rest_framework import serializers

from network.models import Contact, Product, Supplier


class ContactSerializer(serializers.ModelSerializer):
    """Сериализатор для контактов"""
    class Meta:
        model = Contact
        fields = ['id', 'email', 'country', 'city', 'street', 'house_number']


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для продуктов"""
    class Meta:
        model = Product
        fields = ['id', 'name', 'model', 'release_date']


class SupplierSerializer(serializers.ModelSerializer):
    """Полный сериализатор для детального просмотра"""
    contact = ContactSerializer(read_only=True)
    products = ProductSerializer(many=True, read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    supplier_level = serializers.IntegerField(source='supplier.level', read_only=True)

    class Meta:
        model = Supplier
        fields = [
            'id', 'name', 'level', 'contact', 'products',
            'supplier', 'supplier_name', "supplier_level", 'debt', 'created_at'
        ]
        read_only_fields = ['debt', 'created_at']  # Запрещаем обновление debt через API


class SupplierListSerializer(serializers.ModelSerializer):
    """Облегченный сериализатор для списка"""
    city = serializers.CharField(source='contact.city', read_only=True)
    country = serializers.CharField(source='contact.country', read_only=True)
    products_count = serializers.IntegerField(
        source='products.count',
        read_only=True
    )

    class Meta:
        model = Supplier
        fields = [
            'id', 'name', 'level', 'city', 'country',
            'debt', 'products_count', 'created_at'
        ]
        read_only_fields = ['debt', 'created_at']

class SupplierCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и обновления"""
    contact = ContactSerializer()
    products = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Product.objects.all(),
        required=False
    )

    class Meta:
        model = Supplier
        fields = ['name', 'level', 'contact', 'products', 'supplier', 'debt', 'created_at']

    def create(self, validated_data):
        """Создание поставщика вместе с контактами"""
        contact_data = validated_data.pop('contact')
        products = validated_data.pop('products')

        contact = Contact.objects.create(**contact_data)
        supplier = Supplier.objects.create(contact=contact, **validated_data)
        supplier.products.set(products)

        if products:
            supplier.products.set(products)

        return supplier

    def update(self, instance, validated_data):
        """Обновление поставщика и связанных контактов"""
        # Обновление контактов
        if 'contact' in validated_data:
            contact_data = validated_data.pop('contact')
            contact = instance.contact
            for attr, value in contact_data.items():
                setattr(contact, attr, value)
            contact.save()

        # Обновление продуктов
        if 'products' in validated_data:
            products = validated_data.pop('products')
            instance.products.set(products)

        # Обновление остальных полей
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
