from django.db import models
from autoslug import AutoSlugField
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from decimal import Decimal
from .validators import phone_number_validator
from restaurants.models import Restaurant

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
    phone = models.CharField(max_length=10, null=True, blank=False, validators=[phone_number_validator])
    address = models.ManyToManyField('Adress', related_name='customers', blank=True)
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


# menu category model

class Menu_Category (models.Model):
    name = models.CharField(max_length=150, unique=True)
    menu_slug = AutoSlugField(populate_from='name', unique=True, editable=True, blank=True)

    class Meta:
        db_table = 'menu_category'
        verbose_name = 'Menu Category'
        verbose_name_plural = 'Menu Categories'
        app_label = 'fooddelivery'

    def __str__(self):
        return f'{self.name}'

class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menus')
    name = models.CharField(max_length=150)
    price = models.DecimalField(null=False, max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    description = models.TextField(null=False, blank=True)
    category = models.ForeignKey(Menu_Category, on_delete=models.CASCADE, related_name='menu_items')  
    quantity = models.PositiveIntegerField()
    product_image = models.ImageField(upload_to='products/img', null=False, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=False)
    updated_at = models.DateTimeField(auto_now=False)

    class Meta:
        db_table = 'menu'
        verbose_name = 'Menu'
        verbose_name_plural = 'Menus'


    def __str__(self):
        return f"{self.category} - {self.name}"


# cart model

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='carts')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='carts')
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cart'
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
    
    def __str__(self):
        return f'{self.customer.name} - {self.quantity}'
    
    @property
    def total_price(self):
        return self.menu.price * self.quantity

class Adress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_addresses')
    name = models.CharField(max_length=100, null=False, blank=False)
    phone = models.CharField(max_length=10, null=True, blank=False, validators=[phone_number_validator])
    street = models.TextField(null=False, blank=False)
    apartment = models.TextField(null=False, blank=False)
    door_number = models.TextField(null=False, blank=False)
    city = models.CharField(max_length=100, null=False, blank=False)
    postal_code = models.CharField(max_length=10, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'adress'
        verbose_name = 'Adress'
        verbose_name_plural = 'Adresses'

    def __str__(self):
        return f'{self.name} - {self.customer.name}'



class Order(models.Model):
    STATUS = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('delivered', 'Delivered'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")  # Hangi kullanıcının siparişi olduğu
    menu = models.ManyToManyField(Menu, through='OrderItem')  # Hangi ürünlerin siparişte olduğu
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=10, choices=STATUS, default='pending')
    # is_paid = models.BooleanField(default=False)  # Ödeme durumu
    shipping_address = models.ForeignKey(Adress, on_delete=models.CASCADE, related_name='orders_adresses')
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
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitems')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    shipping = models.ForeignKey(Adress, on_delete=models.CASCADE, related_name='orderitems_adresses')

    class Meta:
        db_table = 'order_item'
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f"{self.menu.name} - {self.quantity}"

    @property
    def total_item_price(self):
        return self.menu.price * self.quantity
    



