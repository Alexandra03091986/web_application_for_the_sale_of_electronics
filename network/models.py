from django.core.validators import MinValueValidator
from django.db import models


class Contact(models.Model):
    """Модель контактов"""
    email = models.EmailField(verbose_name="Email")
    country = models.CharField(max_length=100, verbose_name="Страна")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=100, verbose_name="Улица")
    house_number = models.CharField(max_length=20, verbose_name="Номер дома")

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return f"{self.country}, {self.city}, {self.street} {self.house_number}"


class Product(models.Model):
    """Модель продукта"""
    name = models.CharField(max_length=255, verbose_name="Название")
    model = models.CharField(max_length=255, verbose_name="Модель")
    release_date = models.DateField(verbose_name="Дата выхода")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f"{self.name} {self.model}"


class Supplier(models.Model):
    """Модель поставщика"""
    LEVEL_CHOICES = [
        (0, "Завод"),
        (1, "Розничная сеть"),
        (2, "Индивидуальный предприниматель"),
    ]
    name = models.CharField(max_length=255, verbose_name="Название")
    level = models.IntegerField(choices=LEVEL_CHOICES, verbose_name="Уровень сети")
    contact = models.OneToOneField(
        Contact,
        on_delete=models.CASCADE,
        verbose_name="Контакт",
        related_name="supplier"
    )
    products = models.ManyToManyField(Product, verbose_name="Продукты")
    supplier = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Поставщик",
        related_name="clients"
    )
    debt = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Задолженность перед поставщиком"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"

    def __str__(self):
        return self.name
