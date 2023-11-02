from django.shortcuts import render, redirect
from .models import Adress, Cart, Order, OrderItem, Customer, Restaurant, Menu, Menu_Category
from django.http import HttpRequest, JsonResponse
from django.db import transaction
from django.db.utils import IntegrityError
from django.contrib import messages
from .forms import OrderForm, RegisterForm, LoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required



def index(request):
      
    restaurants = Restaurant.objects.all()[:10]

    return render(request, 'index.html', {'restaurants': restaurants})

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


@login_required(login_url='/login')
def profile(request):
    
    customer = request.user
    users = Customer.objects.filter(email=customer.email)
    customer_adress = Adress.objects.filter(customer=request.user)
    order_history = Order.objects.filter(customer=customer).prefetch_related('orderitems__menu').order_by('-created_at')
    context = {'users': users, 'customer_adress': customer_adress, 'order_history': order_history}
    return render(request, 'profile.html', context)


# def order_history(request):
#buraya order item
#     customer = request.user

#     # Kullanıcının sipariş geçmişini al
#     order_history = Order.objects.filter(customer=customer).order_by('-created_at')

#     context = {
#         'order_history': order_history
#     }

#     return render(request, 'order_history.html', context)

    
@login_required(login_url='/login')  # Requires the user to be authenticated
def detailRestaurant(request, name_slug):
    if request.method == "POST":
        return render(request, 'order.html')

    restaurant = Restaurant.objects.get(name_slug=name_slug)
    food_items = Menu.objects.filter(restaurant=restaurant)
    cart_items = Cart.objects.filter(customer=request.user)
    total_price = sum(item.total_price for item in cart_items)
    menu_categories = Menu_Category.objects.filter(menu_items__restaurant=restaurant)
    menu_slugs = [category.menu_slug for category in menu_categories]
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
def add_to_cart(request, menu_id):
    if request.method == "POST":
        try:
            menu = Menu.objects.get(id=menu_id)
            selected_quantity = int(request.POST.get('quantity', 1))

            if menu.quantity < selected_quantity:
                return JsonResponse({"success": False, "message": "Insufficient menu item quantity."})

            cart_item = Cart.objects.filter(customer=request.user, menu=menu).first()

            if cart_item:
                cart_item.quantity += selected_quantity
                cart_item.save()
            else:
                Cart.objects.create(
                    customer=request.user,
                    menu=menu,
                    quantity=selected_quantity
                )
            
            return JsonResponse({"success": True, "message": "Menu item added to cart"})
        
        except (Menu.DoesNotExist, ValueError):
            return JsonResponse({"success": False, "message": "Menu item not found or invalid data."})


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

        for item in cart_items:
            if item.menu.quantity < item.quantity:
                messages.error(request, f"{item.menu.name} doesn't have enough stock.")
                return redirect('cart')

        try:
            with transaction.atomic():
                customer = request.user
                shipping_address = Adress.objects.filter(customer=customer).first()

                if not shipping_address:
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

                order = Order.objects.create(
                    customer=customer,
                    shipping_address=shipping_address,
                    total_price=sum(item.total_price for item in cart_items),
                    status='pending'
                )

                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        menu=item.menu,
                        quantity=item.quantity,
                        shipping_id=shipping_address.id
                    )

                # Update the product's stock quantity
                for item in cart_items:
                    item.menu.quantity -= item.quantity
                    item.menu.save()

                cart_items.delete()

                messages.success(request, 'Your order has been received.')
                return redirect('confirm')  # Specify the target view here

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
