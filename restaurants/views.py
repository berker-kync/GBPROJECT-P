from django.shortcuts import render
from .models import Restaurant, Restaurant_Category
from django.db.models import Count
from django.http import JsonResponse

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




