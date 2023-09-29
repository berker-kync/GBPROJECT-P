from django.shortcuts import render, redirect
from .models import Product, ShoppingCart
from django.http import JsonResponse

def index(request):

    # Ten products list
    products = Product.objects.all()[:10]


    return render(request, 'index.html', {'products': products})

def submitrestaurant(request):
    return render(request, 'submit-restaurant.html')

def detailRestaurant(request):

    products = Product.objects.all()

    # Fetch cart items for this session
    cart_items = ShoppingCart.objects.filter(session_key=request.session.session_key)

    # Calculate the total price
    total_price = sum(item.total_price for item in cart_items)

    context = {
        'products': products,
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'detail-restaurant.html',context)


def add_to_cart(request, product_id):
    if request.method == "POST":
        try:
            product = Product.objects.get(id=product_id)
            selected_quantity = int(request.POST.get('quantity', 1))

            if product.quantity < selected_quantity:
                return JsonResponse({"success": False, "message": "Insufficient product stock."})

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
            # Check if the product is in the cart already
            cart_item = ShoppingCart.objects.filter(session_key=request.session.session_key, id=id).first()

            if cart_item:
                cart_item.delete()  # Remove item from the cart entirely
            else:
                return JsonResponse({"success": False, "message": "Product not found in the cart."})

            return JsonResponse({"success": True, "message": "Product removed from cart."})

        except (Product.DoesNotExist, ValueError):
            return JsonResponse({"success": False, "message": "Product not found or invalid data."})



