from django.shortcuts import render, redirect
from .models import Product, ShoppingCart
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def index(request):

    products = Product.objects.all()[:10]
    return render(request, 'index.html', {'products': products})

def about(request):
    return render(request, 'about.html')

def error_404(request, exception):
    return render(request, '404.html', status=404)

def submitrestaurant(request):
    return render(request, 'submit-restaurant.html')

def detailRestaurant(request):
    products = Product.objects.all()


    cart_items = ShoppingCart.objects.filter(session_key=request.session.session_key)

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


            if not request.session.session_key:
                request.session.save()


            cart_item = ShoppingCart.objects.filter(session_key=request.session.session_key, product=product).first()
            
            if cart_item:

                cart_item.quantity += selected_quantity
                cart_item.save()
            else:

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



def extra_pages(request, page_name):
    content_dict = {
        'about': {
            'page_title': 'HAKKIMIZDA',
            'page_content': 'Çok da bi şey yok aslında.. ',
            'page_image': {'url': '', 'alt': ''}
        },
        'privacy': {
            'page_title': 'GİZLİLİK',
            'page_content': 'Onu söyleyemiyoruz yalnız. ',
            'page_image': {'url': '', 'alt': ''}
        },
        'termsconditions': {
            'page_title': 'ŞARTLAR & KOŞULLAR',
            'page_content': 'TencereKapak LTD. gerektiği taktirde summoning seansları esnasında üyelerinin ruhlarını kurban etmeyi daima saklı tutar. ',
            'page_image': {'url': 'https://m.media-amazon.com/images/I/612+XnLD1RL._AC_UF894,1000_QL80_.jpg', 'alt': 'pentagram'}
        },
        'contacts': {
            'page_title': 'İLETİŞİM',
            'page_content': 'Beni Ara: +90 216-23-221',
            'page_image': {'url': 'https://img.fruugo.com/product/0/26/720275260_max.jpg', 'alt': 'telefon'}
        }
    }
    
    content = content_dict.get(page_name, {'page_title': 'Nau nau', 'page_content': 'Yok ki öyle bi sayfa', 'page_image': {'url': '', 'alt': ''}})

    return render(request, 'extra-pages.html', content)


