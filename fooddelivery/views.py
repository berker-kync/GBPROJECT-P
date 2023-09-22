from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from django.http import JsonResponse

def index(request):
    return render(request, 'index.html')

def submitrestaurant(request):
    return render(request, 'submit-restaurant.html')

def detailRestaurant(request):
    products = Product.objects.all()
    return render(request, 'detail-restaurant.html', {'products': products})

def detailRestaurant2(request):
    products = Product.objects.all()

    food_basket = Product.objects.filter(quantity__gt=0)
    subtotal = sum([product.price for product in food_basket])
    delivery_fee = 10 
    total = subtotal + delivery_fee

    context = {
        'products': products,
        'food_basket': food_basket,
        'delivery_fee': delivery_fee,
        'total': total
    }

    return render(request, 'detail-restaurant-2.html', context)




def increase_quantity(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        product.quantity += 1
        product.save()
        return redirect('detail-restaurant-2')  
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})



