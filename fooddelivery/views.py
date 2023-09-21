from django.shortcuts import render, redirect
from .models import Product, ShoppingCart
from django.http import JsonResponse

def index(request):
    return render(request, 'index.html')

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


# def add_to_cart(request, product_id):
#     if request.method == "POST":
#         try:
#             product = Product.objects.get(id=product_id)
#             selected_quantity = int(request.POST.get('quantity', 1))  # get the quantity from POST data

#             if product.quantity >= selected_quantity:
#                 product.quantity -= selected_quantity
#                 product.save()
#                 return JsonResponse({"success": True, "message": "Product added to cart."})
#             else:
#                 return JsonResponse({"success": False, "message": "Insufficient product stock."})
#         except (Product.DoesNotExist, ValueError):
#             return JsonResponse({"success": False, "message": "Product not found or invalid data."})

def add_to_cart(request, product_id):
    if request.method == "POST":
        try:
            product = Product.objects.get(id=product_id)
            selected_quantity = int(request.POST.get('quantity', 1))

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


# def cart_summary(request):
#     # Fetch cart items for this session
#     cart_items = ShoppingCart.objects.filter(session_key=request.session.session_key)

#     # Calculate the total price
#     total_price = sum(item.total_price for item in cart_items)

#     context = {
#         'cart_items': cart_items,
#         'total_price': total_price,
#     }
    
#     return render(request, 'order_summary.html', context)

