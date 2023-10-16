from re import A
from django.db import models
from autoslug import AutoSlugField
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from decimal import Decimal
from .validators import phone_number_validator


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


# customer model

class CustomerManager(BaseUserManager):
    def create_superuser(self, email, name, password=None):
        if not email:
            raise ValueError("Customers must have an email address")
        if not password:
            raise ValueError("Customers must have a password")
        customer_obj = self.model(
            email=self.normalize_email(email),
            name=name
        )
        customer_obj.set_password(password)
        customer_obj.is_superuser = True
        customer_obj.is_staff = True
        customer_obj.save(using=self._db)
        return customer_obj

    def create_user(self, email, name=None, password=None, is_active=True):
        if not email:
            raise ValueError("Customers must have an email address")
        if not password:
            raise ValueError("Customers must have a password")
        customer_obj = self.model(
            email=self.normalize_email(email),
            name=name
        )
        customer_obj.set_password(password)
        customer_obj.is_active = is_active
        customer_obj.save(using=self._db)
        return customer_obj

class Customer(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(null=False, blank=False, unique=True)
    phone = models.CharField(max_length=20, null=True, blank=False, validators=[phone_number_validator])
    address = models.TextField(null=False, blank=False)
    city = models.CharField(max_length=100, null=False, blank=False)
    postal_code = models.CharField(max_length=10, null=False, blank=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    class Meta:
        db_table = 'customer'
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

    def has_perm(self, perm, obj=None):
        return self.is_staff
    
    def has_module_perms(self, app_label):
        return self.is_staff

    def __str__(self):
        return f'{self.name} - {self.email}'


class Order(models.Model):
    STATUS = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")  # Hangi kullanıcının siparişi olduğu
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
        return f"Order #{self.id} - {self.customer.name}"
    
    @property
    def total_item(self):
        return self.order_items.count()


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
