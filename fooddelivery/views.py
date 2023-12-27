from django.shortcuts import get_object_or_404, render, redirect
from .models import Adress, Cart, Extras, Order, OrderItem, Portion, Restaurant, Menu, Menu_Category, Province
from django.http import JsonResponse
from django.db import transaction
from django.contrib import messages
from .forms import ChangePasswordForm, ChangeUserForm, CustomerAddressForm, RegisterForm, LoginForm, ReviewForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Avg
from restaurants.views import send_email


def index(request):
        
    if request.user.is_staff:
        return user_logout(request)
      
    restaurants = Restaurant.objects.all()[:10]

    return render(request, 'index.html', {'restaurants': restaurants})

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
                messages.success(request, 'Başarıyla giriş yaptınız.')
                
                next_url = request.GET.get('next', 'index')
                return redirect(next_url)
            else:
                messages.error(request, 'Üyeliğiniz aktif değil.')
        else:
            messages.error(request, 'Geçersiz mail ya da şifre.')
            return redirect('login')

    return render(request, 'login.html', {'form': form})

# def user_forget_password(request):
#     form = ForgetPasswordForm(request.POST or None)
#     if request.method == "POST" and form.is_valid():
#         email = form.cleaned_data.get('email')
#         user = User.objects.filter(email=email).first()
#         if user:
#             subject = "Şifre Sıfırlama"
#             message = f"Merhaba {user.name},\n\nŞifrenizi sıfırlamak için aşağıdaki linke tıklayınız:\n\n{request.build_absolute_uri('/reset-password/')}"
#             to_email = user.email

#             send_email(subject, message, to_email)

#             messages.success(request, 'Şifre sıfırlama linki mail adresinize gönderildi.')
#             return redirect('login')
#         else:
#             messages.error(request, 'Böyle bir mail adresi bulunamadı.')
#             return redirect('forget-password')


#     return render(request, 'forget-password.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'Başarıyla çıkış yaptınız.')
    return redirect('index')

def register(request):
    if request.user.is_authenticated:
        return redirect('index')

    form = RegisterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()
        messages.success(request, 'Üyeliğiniz oluşturuldu.')
        
        # Kullanıcıya kayıt maili için
        subject = "TencereKapak'a Hoş Geldiniz!"
        message = f"Merhaba {user.name},\n\nAramıza hoş geldin! Üyeliğin başarıyla oluşturuldu."
        to_email = user.email
        send_email(subject, message, to_email)

        return redirect('login')
    
    return render(request, 'register.html', {'form': form})


def restaurants(request):
    restaurants = Restaurant.objects.all()
    provinces = Province.objects.all()
    return render(request, 'restoranlar.html', {'restaurants': restaurants, 'provinces': provinces})

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

    return render(request, 'change-address.html', {'address_form': address_form})


@login_required(login_url='/login')
def profile(request):
    customer = request.user
    customer_email = customer.email

    # Formların tanımlanması
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
        else:
            messages.error(request, 'Lütfen formu doğru şekilde doldurunuz.')
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

def get_menu_item_details(request):
    menu_id = request.GET.get('menu_id')
    menu_item = Menu.objects.get(id=menu_id)

    portions = list(menu_item.portions.values('name', 'price'))
    extras = list(menu_item.extras.values('name', 'price'))

    return JsonResponse({
        'portions': portions,
        'extras': extras
    })
    
def detailRestaurant(request, name_slug):
    restaurant = Restaurant.objects.get(name_slug=name_slug)
    reviews = restaurant.reviews.all().order_by('-created_at')[:5]
    food_items = Menu.objects.filter(restaurant=restaurant)
    menu_categories = Menu_Category.objects.filter(menu_items__restaurant=restaurant).distinct()
    menu_slugs = [category.menu_slug for category in menu_categories] # Menü kategorilerinin slug'ları yok ki bakalım buna.

    # Kullanıcı giriş yapmışsa ek işlemler
    if request.user.is_authenticated:
        # is_staff sipariş veremesin
        if request.user.is_staff:
            return user_logout(request)

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

        cart_items = Cart.objects.filter(customer=request.user)
        total_price = sum(item.total_price for item in cart_items)
    else:
        cart_items = None
        total_price = 0

    # Ortalama skor ve yorum sayısı hesaplamaları
    average_score = reviews.aggregate(Avg('score'))['score__avg'] if reviews else 0
    review_count = reviews.count()

    context = {
        'food_items': food_items,
        'restaurant': restaurant,
        'reviews': reviews,
        'average_score': round(average_score, 1) if average_score else 'Skor Yok',
        'review_count': review_count,
        'cart_items': cart_items,
        'total_price': total_price,
        'menu_categories': menu_categories,
        'menu_slugs': menu_slugs,
        'is_user_authenticated': request.user.is_authenticated,
    }
    return render(request, 'detail-restaurant.html', context)


@login_required(login_url='/login')
@require_POST
def add_to_cart(request, menu_id):
    menu = get_object_or_404(Menu, id=menu_id)
    portion = request.POST.get('portion')
    extras = request.POST.getlist('extras')
    quantity = int(request.POST.get('quantity'))

    if menu.quantity < quantity:
        return JsonResponse({"success": False, "message": "Yetersiz menü öğesi miktarı.", "toastr_type": "error"})

    # Sepette başka restoranın ürünleri varsa temizle
    cart_items = Cart.objects.filter(customer=request.user)
    if cart_items.exists() and cart_items.first().menu.restaurant != menu.restaurant:
        cart_items.delete()  # Kullanıcının eski sepetini temizle

    portion_instance = Portion.objects.get(id=portion) if portion else None

    # Sepeti oluştur veya güncelle
    cart_item, created = Cart.objects.get_or_create(
        customer=request.user,
        menu=menu,
        portion=portion_instance,
        defaults={'quantity': quantity}
    )

    if created:
        # ManyToManyField için set() metodunu kullan
        cart_item.extras.set(Extras.objects.filter(id__in=extras))
    else:
        # Farklı porsiyon veya ekstralar seçildiyse yeni bir sepet öğesi oluştur
        cart_item = Cart.objects.create(
            customer=request.user,
            menu=menu,
            portion=portion_instance,
            quantity=quantity
        )
        cart_item.extras.set(Extras.objects.filter(id__in=extras))

    cart_item.save()
    
    return JsonResponse({"success": True, "message": "Menü öğesi sepete eklendi", "toastr_type": "success", "cart_item_id": cart_item.id})


@login_required
@require_POST
def update_cart_quantity(request):
    item_id = request.POST.get('itemId')
    new_quantity = int(request.POST.get('quantity'))

    try:
        cart_item = Cart.objects.get(id=item_id, customer=request.user)
        cart_item.quantity = new_quantity
        cart_item.save()

        # Toplam fiyatı hesapla ve JSON yanıtında döndür
        total_price = cart_item.total_price
        total_cart_price = sum(item.total_price for item in Cart.objects.filter(customer=request.user))
        return JsonResponse({'success': True, 'total_price': float(total_price), 'total_cart_price': float(total_cart_price)})
    except Cart.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Sepet öğesi bulunamadı.', "toastr_type": "error"})
    except ValueError:
        return JsonResponse({'success': False, 'error': 'Geçersiz miktar.', "toastr_type": "error"})



@login_required(login_url='/login')  # Requires the user to be authenticated
def remove_from_cart(request, id):
    try:
        # Find the cart item by its ID, associated with the authenticated user (Customer)
        cart_item = Cart.objects.filter(customer=request.user, id=id).first()

        if cart_item:
            # Remove the cart item
            cart_item.delete()
            return JsonResponse({"success": True, "message": "Ürün sepetten silindi.", "toastr_type": "success"})
        else:
            return JsonResponse({"success": False, "message": "Ürün sepette bulunamadı.", "toastr_type": "error"})

    except (Cart.DoesNotExist, ValueError):
        return JsonResponse({"success": False, "message": "Sepet ürünü bulunamadı.", "toastr_type": "success"})


@login_required(login_url='/login')
def order(request):
    customer = request.user
    cart_items = Cart.objects.filter(customer=customer)

    # Check cart items
    if cart_items.exists():
        current_restaurant = cart_items.first().menu.restaurant
        restaurant_province = current_restaurant.province
        addresses = Adress.objects.filter(customer=customer, province=restaurant_province)
    else:
        current_restaurant = None
        addresses = Adress.objects.none()
        messages.error(request, "Sepetiniz boş.")
        return redirect('index')

    total_price = sum(item.total_price for item in cart_items) if cart_items.exists() else 0
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
            messages.error(request, "Lütfen geçerli bir adres seçiniz.")
            return render(request, 'order.html', context)

        for item in cart_items:
            if item.menu.quantity < item.quantity and item.menu.quantity != None:
                messages.error(request, f"{item.menu.name} için yeterli stok miktarı bulunmamaktadır.")
                return render(request, 'order.html', context)

        with transaction.atomic():
            new_order = Order.objects.create(
                customer=customer,
                shipping_address=shipping_address,
                total_price=total_price,
                status='pending',
                payment_method=payment_method,
            )

            order_details = ""
            for item in cart_items:
                # OrderItem nesnesi oluştur
                order_item = OrderItem.objects.create(
                    order=new_order,
                    menu=item.menu,
                    quantity=item.quantity,
                    portion=item.portion,  # Porsiyon bilgisini ekle
                    shipping=shipping_address,
                )
                order_item.extras.set(item.extras.all())  # Ekstraları ekle

                # Ürün stok miktarını güncelle
                item.menu.quantity -= item.quantity
                item.menu.save()

            # Email sending logic
            subject = 'Sipariş Onay'
            message = f'Sevgili {customer.name},\n\nSiparişin restorana ulaştı:\n\nOrder ID: {new_order.id}\n\n{order_details}\nToplam Tutar: {total_price}\n\nBizi tercih ettiğiniz için teşekkür ederiz.'
            to_email = customer.email

            send_email(subject, message, to_email)

            cart_items.delete()
            messages.success(request, 'Siparişiniz başarıyla gerçekleştirildi.')
            return redirect('confirm')

    return render(request, 'order.html', context)



@login_required(login_url='/login')
def confirmorder(request):
    latest_order = Order.objects.filter(customer=request.user).order_by('-created_at').first()

    context = {
        'latest_order': latest_order,
    }

    return render(request, 'confirm.html', context)




@login_required(login_url='/login') 
def review(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)

    # review edilmiş mi
    if order.reviewed:
        messages.error(request, "You have already reviewed this order.")
        return redirect('profile')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.customer = request.user
    
            review.restaurant = order.menu.first().restaurant
            review.order = order
            review.save()

            # review edildi diye kaydet
            order.reviewed = True
            order.save()

            messages.success(request, "Thank you for your review.")
            return redirect('profile')
    else:
        form = ReviewForm()

    restaurant = order.menu.first().restaurant if order.menu.exists() else None

    return render(request, 'leave-review.html', {'form': form, 'order': order, 'restaurant': restaurant})

