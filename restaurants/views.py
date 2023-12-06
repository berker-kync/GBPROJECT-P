import json
import re
from django.shortcuts import get_object_or_404, render, redirect
from fooddelivery.models import Order
from .models import Restaurant, Restaurant_Category, RestaurantRegistration
from fooddelivery.models import Menu, Menu_Category
from restaurants.models import Restaurant
from django.db.models import Count
from django.http import JsonResponse, HttpResponse, QueryDict
from .forms import RestaurantRegistrationForm, MenuItemForm, StaffLoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db.models import F
from django.views.decorators.http import require_POST
import requests
from django.conf import settings




def send_email(subject, text, to_email):
    response = requests.post(
        settings.MAILGUN_SEND_URL,
        auth=("api", settings.MAILGUN_API_KEY),
        data={"from": "TencereKapak <noreply@mail.berkerkoyuncu.xyz>",
              "to": [to_email],
              "subject": subject,
              "text": text})
    
    return response



def partner(request):
    form = RestaurantRegistrationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        new_restaurant = form.save()

        form_data_str = "\n".join(f"{key.title()}: {value}" for key, value in form.cleaned_data.items())
        user_email = form.cleaned_data['email']
        user_name = form.cleaned_data['name']

        # Email to admin or specified email address
        subject1 = "Yeni Partner Restoran Kayıt Bilgisi"
        message1 = f"Yeni bir kayıt formu geldi. İşte detaylar:\n\n{form_data_str}"
        to_email1 = "berkerkoyuncu@gmail.com"  
        send_email(subject1, message1, to_email1)

        # Email to the user who filled the form
        subject2 = "Restoran Kaydınız Alındı"
        message2 = f"Sayın {user_name}, restoran kaydınız başarıyla alınmıştır. En kısa sürede sizinle iletişime geçeceğiz."
        to_email2 = user_email  
        send_email(subject2, message2, to_email2)

        messages.success(request, 'Bilgileriniz bize ulaştı. Sizinle çok yakında iletişim kuracağız :).')
        return redirect(request.path)  

    return render(request, 'partner.html', {'form': form})








def stafflogin(request):
    if request.user.is_authenticated:
        return redirect('adminmain')

    form = StaffLoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        # authenticate() fonksiyonu yalnızca email ve password ile çağrılır
        user = authenticate(request, email=email, password=password)
        
        # Kullanıcının kimlik doğrulaması başarılı mı ve kullanıcı personel mi?
        if user and user.is_staff:
            auth_login(request, user=user)
            messages.success(request, 'You have successfully logged in.')
            return redirect('adminmain')
        else:
            messages.error(request, 'Access denied. Only staff members can log in.') # acaba burası staff yanlis sifre girerse de ayni mi veriyor. mesajı degistirelim mi

    return render(request, 'stafflogin.html', {'form': form})

def stafflogout(request):
    logout(request)
    return redirect('index')





@login_required(login_url='staff-login')
def adminmain(request):
    user = request.user

    if user.is_authenticated and user.is_staff:
        restaurants = Restaurant.objects.filter(manager=request.user)
    else:
        restaurants = Restaurant.objects.none()
        return HttpResponse('Bu sayfayı görüntüleme yetkiniz bulunmamaktadır. Eğer restoran görevlisiyseniz, giriş yapınız.')


    context = {'restaurants': restaurants}
    return render(request, 'adminmain.html', context)




@login_required(login_url='staff-login')
def addtomenu(request):
    restaurant = None
    existing_menu_items = None 

    if hasattr(request.user, 'managed_restaurants'):
        restaurant = request.user.managed_restaurants.first()
        existing_menu_items = Menu.objects.filter(restaurant=restaurant)

    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.restaurant = restaurant 
            menu_item.save()
            messages.success(request, 'Ürün Eklendi')
            form = MenuItemForm() 
    else:
        form = MenuItemForm()

    return render(request, 'addtomenu.html', {'form': form, 'restaurant': restaurant, 'existing_menu_items': existing_menu_items})



@login_required
@require_http_methods(["DELETE"])
def delete_item(request, menu_id):
    menu_item = get_object_or_404(Menu, id=menu_id)
    menu_item.delete()
    return JsonResponse({'success': True, 'message': 'Menu item deleted successfully.'})


@login_required
@require_http_methods(["PATCH"]) 
def toggle_visibility(request, item_id):
    item = get_object_or_404(Menu, id=item_id)
    
    item.is_active = not item.is_active
    item.save()
    
    return JsonResponse({'message': 'Visibility toggled successfully.'})







def panel(request):
    return render(request, 'restaurants-panel.html')


def RestaurantList(request):
    restaurants = Restaurant.objects.all()
    restaurant_categories = Restaurant_Category.objects.annotate(restaurant_count=Count('restaurants'))

    highly_rated_restaurants_9plus = restaurants.filter(score__gte=9.0).count()
    highly_rated_restaurants_8plus = restaurants.filter(score__gte=8.0).count()
    highly_rated_restaurants_7plus = restaurants.filter(score__gte=7.0).count()
    highly_rated_restaurants_6plus = restaurants.filter(score__gte=6.0).count()

    context = {
        'restaurants': restaurants,
        'restaurant_categories': restaurant_categories,
        'highly_rated_restaurants_9plus': highly_rated_restaurants_9plus,
        'highly_rated_restaurants_8plus': highly_rated_restaurants_8plus,
        'highly_rated_restaurants_7plus': highly_rated_restaurants_7plus,
        'highly_rated_restaurants_6plus': highly_rated_restaurants_6plus,
    }

    return render(request, 'restaurant-list.html', context)



def filter_restaurants(request):
    selected_categories = request.POST.getlist('categories')
    filtered_restaurants = Restaurant.objects.filter(category__in=selected_categories)

    filtered_data = [{'name': restaurant.name, 'category': restaurant.category.name, 'score': restaurant.score} for restaurant in filtered_restaurants]

    return JsonResponse({'filtered_restaurants': filtered_restaurants})




@login_required
def order_list(request):
    orders = Order.objects.filter(orderitems__menu__restaurant__manager=request.user).distinct()
    return render(request, 'order_list.html', {'orders': orders})


@login_required
@require_http_methods(["PATCH"])
def update_order_status(request, order_id):
    if not request.user.is_staff:
        return JsonResponse({'status': 'error', 'message': 'Yetkiniz yok'}, status=403)

    order = get_object_or_404(Order, id=order_id)


    if not request.user.managed_restaurants.filter(
    menus__order=order).exists():
        return JsonResponse({'status': 'error', 'message': 'Bu işlem için yetkiniz yok'}, status=403)


    data = json.loads(request.body.decode('utf-8'))
    status = data.get('status')

    if status in dict(Order.STATUS).keys():
        if status == 'rejected' and not order.status == 'rejected':
            for item in order.orderitems.all():
                item.menu.quantity = F('quantity') + item.quantity
                item.menu.save()

        order.status = status
        order.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Geçersiz durum değeri'}, status=400)

