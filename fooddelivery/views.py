from calendar import c
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Cart, Order, OrderItem
from django.http import HttpRequest, JsonResponse
from django.contrib import messages
from .forms import OrderForm, RegisterForm, LoginForm
from django.db import transaction  # İşlemleri atomik bir şekilde yürütmek için
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required


def index(request):
      
    products = Product.objects.all()[:10]

    return render(request, 'index.html', {'products': products})

def Login(request):
    if request.user.is_authenticated:
        return redirect('index')

    form = LoginForm(request.POST or None)
    
    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        customer = authenticate(request, email=email, password=password)
        if customer and not customer.is_superuser:
            login(request, user=customer)
            messages.success(request, 'You have successfully logged in.')
            return redirect('index')
        else:
            messages.error(request, 'Invalid email or password.')

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
        # if you want to login response after register
        return HttpRequest('/login')

    return render(request, 'register.html', {'form': form})

@login_required
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



@login_required  # Requires the user to be authenticated
def detailRestaurant(request):
    if request.method == "POST":
        return render(request, 'order.html')

    products = Product.objects.all()
    cart_items = Cart.objects.filter(customer=request.user)
    total_price = sum(item.total_price for item in cart_items)
    context = {
        'products': products,
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'detail-restaurant.html', context)


@login_required  # Requires the user to be authenticated
def add_to_cart(request, product_id):
    if request.method == "POST":
        try:
            product = Product.objects.get(id=product_id)
            selected_quantity = int(request.POST.get('quantity', 1))

            if product.quantity < selected_quantity:
                return JsonResponse({"success": False, "message": "Insufficient product quantity."})

            # Check if the product is in the cart already
            cart_item = Cart.objects.filter(customer=request.user, product=product).first()

            if cart_item:
                # Update the quantity of the existing cart item
                cart_item.quantity += selected_quantity
                cart_item.save()
            else:
                # Create a new cart item
                Cart.objects.create(
                    customer=request.user,
                    product=product,
                    quantity=selected_quantity
                )
            
            return JsonResponse({"success": True, "message": "Product added to cart"})
        
        except (Product.DoesNotExist, ValueError):
            return JsonResponse({"success": False, "message": "Product not found or invalid data."})


@login_required  # Requires the user to be authenticated
def remove_from_cart(request, id):
    try:
        # Find the cart item by its ID, associated with the authenticated user (Customer)
        cart_item = Cart.objects.filter(customer=request.user, id=id).first()

        if cart_item:
            # Remove the cart item
            cart_item.delete()
            return JsonResponse({"success": True, "message": "Product removed from cart."})
        else:
            return JsonResponse({"success": False, "message": "Product not found in the cart."})

    except (Cart.DoesNotExist, ValueError):
        return JsonResponse({"success": False, "message": "Cart item not found or invalid data."})



@login_required  # Requires the user to be authenticated
def order(request):
    form = OrderForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        cart_items = Cart.objects.filter(customer=request.user)

        # Check if there is enough stock for each product in the cart
        for item in cart_items:
            if item.product.quantity < item.quantity:
                messages.error(request, f"{item.product.name} doesn't have enough stock.")
                return redirect('cart')  # Redirect to the cart page or any other appropriate action

        # If there is enough stock, complete the order
        with transaction.atomic():  # Ensures that all operations within this block are successful
            # Get the authenticated user (Customer) for the order
            customer = request.user

            # Create a new order
            order = Order.objects.create(
                customer=customer,
                shipping_address=customer.address,
                total_price=sum(item.total_price for item in cart_items),
                status='pending'
            )

            # Create order items
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity
                )

                # Update the product's stock quantity
                item.product.quantity -= item.quantity
                item.product.save()

            # Clear the cart
            cart_items.delete()

            messages.success(request, 'Your order has been received.')
            return redirect('confirm')

    cart_items = Cart.objects.filter(customer=request.user)
    total_price = sum(item.total_price for item in cart_items)
    context = {'cart_items': cart_items, 'total_price': total_price, 'form': form}
    return render(request, 'order.html', context)




def confirmorder(request):
    return render(request, 'confirm.html')
