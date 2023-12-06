from django.shortcuts import get_object_or_404, render, redirect
from .models import Adress, Cart, Order, OrderItem, Restaurant, Menu, Menu_Category, Province
from django.http import JsonResponse
from django.db import transaction
from django.contrib import messages
from .forms import ChangePasswordForm, ChangeUserForm, CustomerAddressForm, RegisterForm, LoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


def index(request):
      
    restaurants = Restaurant.objects.all()[:10]

    provinces = Province.objects.all()

    return render(request, 'index.html', {'restaurants': restaurants, 'provinces': provinces})

def Login(request):
    if request.user.is_authenticated:
        return redirect('index')

    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        user = authenticate(request, email=email, password=password)
        
        if user is not None and not (user.is_staff or user.is_superuser):
            if user.is_active:
                login(request, user)
                messages.success(request, 'You have successfully logged in.')
                return redirect('index')
            else:
                messages.error(request, 'Your account is inactive.')
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('login')

    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('index')

def register(request):
    if request.user.is_authenticated:
        return redirect('index')

    form = RegisterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, 'Your account has been created.')
        return redirect('login')
    
    return render(request, 'register.html', {'form': form})


def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def termsconditions(request):
    return render(request, 'termsconditions.html')

def privacy(request):
    return render(request, 'privacy.html')

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def delete_address(request, address_id):
    address = get_object_or_404(Adress, id=address_id)
    address.delete()
    messages.success(request, 'Adresiniz silinmiştir.')
    return redirect('profile')

def edit_address(request, address_id):
    address = get_object_or_404(Adress, id=address_id)

    if request.method == "POST":
        address_form = CustomerAddressForm(request.POST, instance=address)
        if address_form.is_valid():
            if address_form.has_changed():
                address_form.save()
                messages.success(request, 'Adresiniz güncellenmiştir.')
                return redirect('profile')
            else:
                messages.info(request, 'Hiçbir değişiklik yapılmadı.')
                return redirect('profile')
    else:
        address_form = CustomerAddressForm(instance=address)

    return render(request, 'change_address.html', {'address_form': address_form})

@login_required(login_url='/login')
def profile(request):
    customer = request.user
    customer_email = customer.email

    # Formlarınızın tanımlanması
    user_form = ChangeUserForm(request.POST or None, instance=request.user)
    user_password_form = ChangePasswordForm(request.user, request.POST or None)
    customer_adress = Adress.objects.filter(customer=request.user)
    address_count = customer.customer_addresses.count()
    can_add_more_addresses = address_count < 5
    address_form = CustomerAddressForm(request.POST or None) if can_add_more_addresses else None

    # Profil Bilgileri Formu Kontrolü
    if 'profile_form' in request.POST:
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Profil bilgileriniz güncellenmiştir.')
            return redirect('profile')

    # Şifre Değiştirme Formu Kontrolü
    elif 'password_form' in request.POST:
        if user_password_form.is_valid():
            user_password_form.save()
            messages.success(request, 'Şifreniz güncellenmiştir.')
            return redirect('profile')

    # Adres Ekleme Formu Kontrolü
    elif 'address_form' in request.POST and can_add_more_addresses:
        if address_form.is_valid():
            address = address_form.save(commit=False)
            address.customer = customer
            address.save()
            messages.success(request, 'Adresiniz eklendi.')
            return redirect('profile')

    order_history = Order.objects.filter(customer=customer).prefetch_related('orderitems__menu').order_by('-created_at')

    context = {
        'customer_email': customer_email, 
        'customer_adress': customer_adress, 
        'order_history': order_history, 
        'form': address_form, 
        'can_add_more_addresses': can_add_more_addresses, 
        'address_count': address_count, 
        'user_form': user_form,
        'user_password_form': user_password_form,
    }

    return render(request, 'profile.html', context)


# def get_province(request, province_slug):
#     province = get_object_or_404(Province, province_slug=province_slug)
#     restaurants = Restaurant.objects.filter(province=province)
#     return render(request, 'province.html', {'restaurants': restaurants, 'province': province})
    
@login_required(login_url='/login') 
def detailRestaurant(request, name_slug):
    # is_staff sipariş veremesin
    if request.user.is_staff:
        return redirect('index')

    if request.method == "POST":
        # Sepetin dolu olup olmadığını kontrol et
        cart_items = Cart.objects.filter(customer=request.user)
        if not cart_items.exists():
            # Eğer sepet boşsa, kullanıcıya hata mesajı göster
            messages.error(request, 'Sepetiniz boş.')
            return redirect('detail-restaurant', name_slug=name_slug)
        else:
            # Sepet doluysa, kullanıcıyı 'order' sayfasına yönlendir
            return redirect('order')
    
    restaurant = Restaurant.objects.get(name_slug=name_slug)
    food_items = Menu.objects.filter(restaurant=restaurant)
    cart_items = Cart.objects.filter(customer=request.user)
    total_price = sum(item.total_price for item in cart_items)
    menu_categories = Menu_Category.objects.filter(menu_items__restaurant=restaurant).distinct()
    menu_slugs = [category.menu_slug for category in menu_categories]


    context = {
        'food_items': food_items,
        'restaurant': restaurant,
        'cart_items': cart_items,
        'total_price': total_price,
        'menu_categories': menu_categories,
        'menu_slugs': menu_slugs,
    }
    return render(request, 'detail-restaurant.html', context)



@login_required(login_url='/login')
@require_POST  # Bu dekoratör fonksiyonun yalnızca POST istekleri ile çağrılmasını sağlar.
def add_to_cart(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    selected_quantity = int(request.POST.get('quantity', 1))

    if menu.quantity < selected_quantity:
        return JsonResponse({"success": False, "message": "Yetersiz menü öğesi miktarı."})
    
    # Sepette başka restoranın ürünleri varsa temizle
    cart_items = Cart.objects.filter(customer=request.user)
    if cart_items.exists() and cart_items.first().menu.restaurant != menu.restaurant:
        cart_items.delete()  # Kullanıcının eski sepetini temizle

    # Sepete yeni ürün ekle veya var olanı güncelle
    cart_item, created = Cart.objects.get_or_create(customer=request.user, menu=menu)
    if not created:
        if menu.quantity < (cart_item.quantity + selected_quantity):
            return JsonResponse({"success": False, "message": "Yetersiz menü öğesi miktarı."})
        cart_item.quantity += selected_quantity
        cart_item.save()
    else:
        cart_item.quantity = selected_quantity
        cart_item.save()

    return JsonResponse({"success": True, "message": "Menü öğesi sepete eklendi"})




@login_required(login_url='/login')  # Requires the user to be authenticated
def remove_from_cart(request, id):
    try:
        # Find the cart item by its ID, associated with the authenticated user (Customer)
        cart_item = Cart.objects.filter(customer=request.user, id=id).first()

        if cart_item:
            # Remove the cart item
            cart_item.delete()
            return JsonResponse({"success": True, "message": "Ürün sepetten silindi."})
        else:
            return JsonResponse({"success": False, "message": "Ürün sepette bulunamadı."})

    except (Cart.DoesNotExist, ValueError):
        return JsonResponse({"success": False, "message": "Sepet ürünü bulunamadı."})


# order verdikten sonra rejected olursa database deki quantity'yi geri almak için ne yapacağız?
# ödeme yöntemlerini modellere eklemek gerekiyor.

@login_required(login_url='/login')
def order(request):
    customer = request.user
    cart_items = Cart.objects.filter(customer=request.user)
    current_restaurant = Cart.objects.filter(customer=request.user).select_related('menu__restaurant')
    total_price = sum(item.total_price for item in cart_items)
    addresses = Adress.objects.filter(customer=customer)
    payment_method = request.POST.get('payment_method', 'nakit')
    context = {
        'addresses': addresses,
        'cart_items': cart_items,
        'total_price': total_price,
        'current_restaurant': current_restaurant,
    }

    if request.method == "POST":
        selected_address_id = request.POST.get('address')
        shipping_address = Adress.objects.filter(id=selected_address_id).first()

        if not shipping_address:
            messages.error(request, "Lütfen gerçerli bir adres seçiniz.")
            return redirect('restaurant-list')

        cart_items = Cart.objects.filter(customer=customer)
        if not cart_items.exists():
            messages.error(request, "Sepetiz boş.")
            return redirect('restaurant-list')

        for item in cart_items:
            if item.menu.quantity < item.quantity and item.menu.quantity != None:
                messages.error(request, f"{item.menu.name} için yeterli stok miktarı bulunmamaktadır.")
                return render(request, 'order.html', context)

        with transaction.atomic():
            order = Order.objects.create(
                customer=customer,
                shipping_address=shipping_address,
                total_price=sum(item.total_price for item in cart_items),
                status='pending',
                payment_method=payment_method,

            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    menu=item.menu,
                    quantity=item.quantity,
                    shipping=shipping_address,
                )
                item.menu.quantity -= item.quantity
                item.menu.save()

            cart_items.delete()
            messages.success(request, 'Siparişiniz başarıyla gerçekleştirildi.')
            return redirect('confirm')
    
    cart_items = Cart.objects.filter(customer=customer)
    if not cart_items.exists():
        messages.error(request, "Sepetiniz boş.")
        return redirect('restaurant-list')

    return render(request, 'order.html', context)



@login_required(login_url='/login')
def confirmorder(request):
    latest_order = Order.objects.filter(customer=request.user).order_by('-created_at').first()

    context = {
        'latest_order': latest_order,
    }

    return render(request, 'confirm.html', context)

