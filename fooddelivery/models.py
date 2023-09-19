from django.db import models
from autoslug import AutoSlugField
from django.core.validators import MinValueValidator
from decimal import Decimal

class Product(models.Model):
    name = models.CharField(max_length=255)
    name_slug = AutoSlugField(populate_from='name', unique=True, editable=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'product'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


    def __str__(self):
        return f'{self.name} - ₺{self.price}'
    



