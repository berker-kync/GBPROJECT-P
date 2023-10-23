from django.shortcuts import render, redirect, get_object_or_404
from .models import Adress, Product, Cart, Order, OrderItem
from django.http import HttpRequest, JsonResponse
from django.db import transaction
from django.db.utils import IntegrityError
from django.contrib import messages
from .forms import OrderForm, RegisterForm, LoginForm
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



@login_required(login_url='/login')  # Requires the user to be authenticated
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


@login_required(login_url='/login')  # User login olmasını saglar.
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


@login_required(login_url='/login')  # Requires the user to be authenticated
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



@login_required(login_url='/login')
def order(request):
    form = OrderForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        cart_items = Cart.objects.filter(customer=request.user)

        # Check if there is enough stock for each product in the cart
        for item in cart_items:
            if item.product.quantity < item.quantity:
                messages.error(request, f"{item.product.name} doesn't have enough stock.")
                return redirect('cart')

        try:
            with transaction.atomic():
                # Get the authenticated user (Customer) for the order
                customer = request.user

                # if shipping address exists don't create a new one
                shipping_address = Adress.objects.filter(customer=customer).first()

                if not shipping_address:
                    # Create a new shipping address
                    shipping_address = Adress.objects.create(
                        customer=customer,
                        name=form.cleaned_data.get('name'),
                        phone=form.cleaned_data.get('phone'),
                        street=form.cleaned_data.get('street'),
                        apartment=form.cleaned_data.get('apartment'),
                        door_number=form.cleaned_data.get('door_number'),
                        city=form.cleaned_data.get('city'),
                        postal_code=form.cleaned_data.get('postal_code')
                    )

                # Create a new order
                order = Order.objects.create(
                    customer=customer,
                    shipping_address=shipping_address,
                    total_price=sum(item.total_price for item in cart_items),
                    status='pending'
                )

                # Create order items
                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        shipping_id=shipping_address.id
                    )

                # Update the product's stock quantity
                for item in cart_items:
                    item.product.quantity -= item.quantity
                    item.product.save()

                # Clear the cart
                cart_items.delete()

                messages.success(request, 'Your order has been received.')
                return redirect('confirm')
        except IntegrityError as e:
            # Rollback the transaction in case of an error
            transaction.set_rollback(True)

            # Display an error message to the user
            messages.error(request, f"An error occurred while processing your order: {e}")
            return redirect('order')

    cart_items = Cart.objects.filter(customer=request.user)
    total_price = sum(item.total_price for item in cart_items)
    context = {'cart_items': cart_items, 'total_price': total_price, 'form': form}
    return render(request, 'order.html', context)




def confirmorder(request):
    return render(request, 'confirm.html')
