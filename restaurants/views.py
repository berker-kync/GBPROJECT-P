from django.shortcuts import render, redirect
from .models import Restaurant, Restaurant_Category, RestaurantRegistration
from django.db.models import Count
from django.http import JsonResponse, HttpResponse
from .forms import RestaurantRegistrationForm, MenuItemForm, StaffLoginForm
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.decorators import login_required



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



def partner(request):
    form = RestaurantRegistrationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, 'Your account has been created.')
        return redirect('index')
    
    return render(request, 'partner.html', {'form': form})



@login_required
def adminmain(request):
    restaurants = Restaurant.objects.filter(manager=request.user)

    context = {'restaurants': restaurants}
    return render(request, 'adminmain.html', context)




@login_required
def addtomenu(request):
    restaurant = None
    if hasattr(request.user, 'managed_restaurants'):
        restaurant = request.user.managed_restaurants.first()

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

    return render(request, 'addtomenu.html', {'form': form, 'restaurant': restaurant})









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



