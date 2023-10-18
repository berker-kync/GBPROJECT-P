from django.db import models
from autoslug import AutoSlugField
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from decimal import Decimal

# from fooddelivery.models import Category



class Restaurant_Category (models.Model):
    name = models.CharField(max_length=150, unique=True, null=True)

    class Meta:
        app_label = 'fooddelivery'

    class Meta:
        db_table = 'restaurant_category'
        verbose_name = 'Restaurant Category'
        verbose_name_plural = 'Restaurant Categories'

    def __str__(self) -> str:
        return f'{self.name}'


class Restaurant(models.Model):
    name = models.CharField(max_length=150)
    name_slug = AutoSlugField(populate_from='name', unique=True, editable=True, blank=True)
    category = models.ForeignKey(Restaurant_Category, on_delete=models.CASCADE, related_name='restaurants', blank=True, null=True)
    score = models.DecimalField(max_digits=3, decimal_places=1, validators=[MinValueValidator(Decimal('0.1')), MaxValueValidator(Decimal('10.0'))])
    restaurant_image = models.ImageField(upload_to='restaurant/img', null=True, blank=True)
    address = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10, validators=[RegexValidator(regex='^\d{10}$')], blank=True)
    delivery_fee = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    payment_methods = models.CharField(max_length=255)
    opening_hour = models.TimeField(null=True)
    closing_hour = models.TimeField(null=True)
    minimum_order_amount = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'restaurant'
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurants'

    def __str__(self):
        return f'{self.name} - {self.category}'
