from django.db import models
from autoslug import AutoSlugField
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from decimal import Decimal
from django.conf import settings

# from fooddelivery.models import Category



class Restaurant_Category (models.Model):
    name = models.CharField(max_length=150, unique=True)

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
    category = models.ForeignKey(Restaurant_Category, on_delete=models.CASCADE, related_name='restaurants')
    score = models.DecimalField(max_digits=3, decimal_places=1, validators=[MinValueValidator(Decimal('0.1')), MaxValueValidator(Decimal('10.0'))])
    restaurant_image = models.ImageField(upload_to='restaurant/img')
    address = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10, validators=[RegexValidator(regex='^\d{10}$')])
    delivery_fee = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    payment_methods = models.CharField(max_length=255)
    opening_hour = models.TimeField()
    closing_hour = models.TimeField()
    minimum_order_amount = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    is_open = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='managed_restaurants',null=True, blank=True,limit_choices_to={'is_staff': True} )

    class Meta:
        db_table = 'restaurant'
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurants'

    def __str__(self):
        return f'{self.name} - {self.category}'


class RestaurantRegistration(models.Model):
    email = models.EmailField(null=False, blank=False, unique=True, editable=True)
    name = models.CharField(max_length=150, null=False, blank=False, editable=True)
    restaurant_name = models.CharField(max_length=150, null=False, blank=False, unique=True, editable=True)
    address = models.CharField(max_length=255, null=False, blank=False, editable=True)
    province = models.CharField(max_length=50, null=False, blank=False, editable=True)
    postal_code = models.CharField(max_length=5, null=False, blank=False, editable=True)

    class Meta:
        db_table = 'restaurant_registration'
        verbose_name = 'RestaurantRegistration'
        verbose_name_plural = 'RestaurantRegistrations'

    def __str__(self):
        return f'{self.restaurant_name}'
       