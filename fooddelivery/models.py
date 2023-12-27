from django.db import models
from autoslug import AutoSlugField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from decimal import Decimal
from .validators import phone_number_validator
from restaurants.models import Restaurant, Province
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# customer model

class CustomerManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class Customer(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(null=False, blank=False, unique=True)
    phone = models.CharField(max_length=10, null=True, blank=False, validators=[phone_number_validator])
    address = models.ManyToManyField('Adress', related_name='customers', blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomerManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        ordering = ['email']
        db_table = 'customer'
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'
        app_label = 'fooddelivery'

    def __str__ (self):
        return self.email
    
    def has_module_perms(self, app_label):
        return self.is_superuser

    def has_perm(self, perm, obj=None):
        return self.is_superuser


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
        return self.name

class Extras(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False)
    price = models.DecimalField(null=False, max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    
    class Meta:
        db_table = 'extras'
        verbose_name = 'Extra'
        verbose_name_plural = 'Extras'

    def __str__(self):
        return f'{self.name}'

    

class Extracategory(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False)
    extras = models.ManyToManyField(Extras, related_name='extra_categories')

    class Meta:
        db_table = 'extra_category'
        verbose_name = 'Extra Category'
        verbose_name_plural = 'Extra Categories'

    def __str__(self):
        return f'{self.name}'
    

class Portion(models.Model):
    name = models.CharField(max_length=30, null=False, blank=False)
    price = models.DecimalField(null=False, max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])

    class Meta:
        db_table = 'portions'
        verbose_name = 'Portion'
        verbose_name_plural = 'Portions'

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
    extras = models.ManyToManyField(Extras, related_name='menus', blank=True)
    portions = models.ManyToManyField(Portion, related_name='menus', blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'menu'
        verbose_name = 'Menu'
        verbose_name_plural = 'Menus'


    def __str__(self):
        return f"{self.name}"
    
    # @property
    # def total_price(self):
    #     return (self.price + self.extras.price + self.portions.price)* self.quantity


# cart model

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='carts')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='carts')
    quantity = models.PositiveIntegerField(default=1)
    portion = models.ForeignKey(Portion, on_delete=models.SET_NULL, null=True, blank=True)
    extras = models.ManyToManyField(Extras, blank=True)
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
        total_price = self.menu.price
        if self.portion:
            total_price += self.portion.price
        for extra in self.extras.all():
            total_price += extra.price
        return total_price * self.quantity


class Adress(models.Model):

    CITY_CHOICES = [
        ('İstanbul', 'İstanbul'),
    ]
        
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_addresses')
    name = models.CharField(max_length=100, null=False, blank=False)
    phone = models.CharField(max_length=10, null=True, blank=False, validators=[phone_number_validator])
    street = models.TextField(null=False, blank=False)
    apartment = models.TextField(null=False, blank=False)
    door_number = models.TextField(null=False, blank=False)
    city = models.CharField(max_length=100, choices=CITY_CHOICES, default=None, null=False, blank=False)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='province_addresses')
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
    payment_method = models.CharField(max_length=100, null=False, blank=False, default='nakit')
    reviewed = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders') confirm sayfasında restoran ismi göstermek için gerekebilir

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
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='menus')
    quantity = models.PositiveIntegerField()
    portion = models.ForeignKey(Portion, on_delete=models.SET_NULL, null=True, blank=True)
    extras = models.ManyToManyField(Extras, blank=True)
    shipping = models.ForeignKey(Adress, on_delete=models.CASCADE, related_name='orderitems_adresses')


    class Meta:
        db_table = 'order_item'
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return f"{self.menu.name} - {self.quantity}"

    @property
    def total_item_price(self):
        total_price = self.menu.price
        if self.portion:
            total_price += self.portion.price
        for extra in self.extras.all():
            total_price += extra.price
        return total_price * self.quantity



# REVIEW DENEMESİ

class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='reviews', null="True")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField()
    score = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(Decimal('0.1')), MaxValueValidator(Decimal('10.0'))])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'review'
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return f' {self.restaurant.name} restoranı için {self.customer.name} yorumu'

