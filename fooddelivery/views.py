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
    return render(request, 'detail-restaurant-2.html', {'products': products})

def deneme(request):
    products = Product.objects.all()
    return render(request, 'deneme.html', {'products': products})

def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, pk=product_id)
        
        order = Order(product=product, quantity=quantity)
        order.save()

def increase_quantity(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        product.quantity -= 1
        product.save()
        return JsonResponse({'success': True, 'new_quantity': product.quantity})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

def your_view_function(request):
    products_in_basket = Product.objects.filter(quantity__gt=0)
    subtotal = sum([product.price for product in products_in_basket])
    delivery_fee = 10 
    total = subtotal + delivery_fee

    return render(request, 'your_template.html', {
        'products_in_basket': products_in_basket,
        'subtotal': subtotal,
        'delivery_fee': delivery_fee,
        'total': total
    })
