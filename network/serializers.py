from rest_framework import serializers

from network.models import Contact, Product, Supplier


class ContactSerializer(serializers.ModelSerializer):
    """"""
    class Meta:
        model = Contact
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """"""
    class Meta:
        model = Product
        fields = '__all__'


class SupplierSerializer(serializers.ModelSerializer):
    """"""
    contact = ContactSerializer(read_only=True)
    products = ProductSerializer(many=True, read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)

    class Meta:
        model = Supplier
        fields = [
            'id', 'name', 'level', 'contact', 'products',
            'supplier', 'supplier_name', 'debt', 'created_at'
        ]
        read_only_fields = ['debt', 'created_at']  # Запрещаем обновление debt через API


class SupplierCreateUpdateSerializer(serializers.ModelSerializer):
    """"""
    contact = ContactSerializer()
    products = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Product.objects.all()
    )

    class Meta:
        model = Supplier
        fields = ['name', 'level', 'contact', 'products', 'supplier', 'debt', 'created_at']
        read_only_fields = ['debt', 'created_at']

    def create(self, validated_data):
        contact_data = validated_data.pop('contact')
        products = validated_data.pop('products')

        contact = Contact.objects.create(**contact_data)
        supplier = Supplier.objects.create(contact=contact, **validated_data)
        supplier.products.set(products)

        return supplier

    def update(self, instance, validated_data):
        if 'contact' in validated_data:
            contact_data = validated_data.pop('contact')
            contact = instance.contact
            for attr, value in contact_data.items():
                setattr(contact, attr, value)
            contact.save()

        if 'products' in validated_data:
            products = validated_data.pop('products')
            instance.products.set(products)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
