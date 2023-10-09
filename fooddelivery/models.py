from django.db import models
from autoslug import AutoSlugField
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=255)
    name_slug = AutoSlugField(populate_from='name', unique=True, editable=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    description = models.TextField()
    product_image = models.ImageField(upload_to='products/img', null=True, blank=True)
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


# cart model

class ShoppingCart(models.Model):
    session_key = models.CharField(max_length=255, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'shopping_cart'
        verbose_name = 'Shopping Cart'
        verbose_name_plural = 'Shopping Carts'

    def __str__(self):
        return f'{self.product.name} - {self.quantity}'

    @property
    def total_price(self):
        return self.product.price * self.quantity
    

# order model

# class Order(models.Model):
#     STATUS = (
#         ('pending', 'Pending'),
#         ('approved', 'Approved'),
#         ('rejected', 'Rejected'),
#     )
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     total_price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
#     status = models.CharField(max_length=10, choices=STATUS, default='pending')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     class Meta:
#         db_table = 'order'
#         verbose_name = 'Order'
#         verbose_name_plural = 'Orders'

#     def __str__(self):
#         return f'{self.user.username} - {self.total_price} - {self.status}'

class Order(models.Model):
    STATUS = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")  # Hangi kullanıcının siparişi olduğu
    products = models.ManyToManyField(Product, through='OrderItem')  # Hangi ürünlerin siparişte olduğu
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=10, choices=STATUS, default='pending')
    # is_paid = models.BooleanField(default=False)  # Ödeme durumu
    shipping_address = models.TextField()  # Gönderim adresi
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'order'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        db_table = 'order_item'
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    @property
    def total_item_price(self):
        return self.product.price * self.quantity
