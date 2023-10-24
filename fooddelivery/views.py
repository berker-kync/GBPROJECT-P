from math import e
from os import name
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, ShoppingCart, Order, OrderItem, Restaurant, Restaurant_Category, Menu
from django.http import JsonResponse
from django.contrib import messages
from .forms import OrderForm
from django.db import transaction  # İşlemleri atomik bir şekilde yürütmek için




def index(request):
    products = Product.objects.all()[:10]
    return render(request, 'index.html', {'products': products})

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




def detailRestaurant(request, name_slug):
    if request.method == "POST":
        return render(request, 'order.html')

    restaurant = Restaurant.objects.get(name_slug=name_slug)
    food_items = Menu.objects.filter(restaurant=restaurant)
    cart_items = ShoppingCart.objects.filter(session_key=request.session.session_key)
    total_price = sum(item.total_price for item in cart_items)
    context = {
        'food_items': food_items,
        'restaurant': restaurant,
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'detail-restaurant.html', context)


    


def add_to_cart(request, product_id):
    if request.method == "POST":
        try:
            product = Product.objects.get(id=product_id)
            selected_quantity = int(request.POST.get('quantity', 1))

            if product.quantity < selected_quantity:
                return JsonResponse({"success": False, "message": "Insufficient product quantity."})

            # Create a session if it doesn't exist
            if not request.session.session_key:
                request.session.save()

            # Check if the product is in the cart already
            cart_item = ShoppingCart.objects.filter(session_key=request.session.session_key, product=product).first()
            
            if cart_item:
                # Update the quantity
                cart_item.quantity += selected_quantity
                cart_item.save()
            else:
                # Create a new cart item
                ShoppingCart.objects.create(
                    product=product,
                    quantity=selected_quantity,
                    session_key=request.session.session_key
                )
            
            return JsonResponse({"success": True, "message": "Product added to cart."})
        
        except (Product.DoesNotExist, ValueError):
            return JsonResponse({"success": False, "message": "Product not found or invalid data."})

def remove_from_cart(request, id):
    if request.method == "POST":
        try:

            cart_item = ShoppingCart.objects.filter(session_key=request.session.session_key, id=id).first()

            if cart_item:
                cart_item.delete()  
            else:
                return JsonResponse({"success": False, "message": "Product not found in the cart."})

            return JsonResponse({"success": True, "message": "Product removed from cart."})

        except (Product.DoesNotExist, ValueError):
            return JsonResponse({"success": False, "message": "Product not found or invalid data."})


def order(request):
    form = OrderForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        cart_items = ShoppingCart.objects.filter(session_key=request.session.session_key)

        # Stokta yeterli ürün olup olmadığını kontrol edelim
        for item in cart_items:
            if item.product.quantity < item.quantity:
                messages.error(request, f"{item.product.name} için stokta yeterli ürün yok.")
                return redirect('cart')  # Veya ilgili URL'ye yönlendirme yapabilirsiniz

        # Eğer yeterli stok varsa siparişi tamamla
        with transaction.atomic():  # Bu bloktaki işlemlerin tümünün başarılı olmasını sağlar
            # Yeni bir müşteri oluştur
            customer = form.save()

            # Yeni bir sipariş oluştur
            order = Order.objects.create(
                customer=customer,
                shipping_address=customer.address,
                total_price=sum(item.total_price for item in cart_items),
                status='pending'
            )

            # Sipariş ürünlerini oluştur
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity
                )

                # Ürün stok adedini güncelle
                item.product.quantity -= item.quantity
                item.product.save()

            # Sepeti temizle
            cart_items.delete()

            messages.success(request, 'Your order has been received.')
            return redirect('confirm')

    cart_items = ShoppingCart.objects.filter(session_key=request.session.session_key)
    total_price = sum(item.total_price for item in cart_items)
    context = {'cart_items': cart_items, 'total_price': total_price, 'form': form}
    return render(request, 'order.html', context)


def confirmorder(request):
    return render(request, 'confirm.html')
