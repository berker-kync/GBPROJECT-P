from math import e
from os import name
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, ShoppingCart, Order, OrderItem
from django.http import JsonResponse
from django.contrib import messages
from .forms import OrderForm
from django.db import transaction  # İşlemleri atomik bir şekilde yürütmek için
from django.shortcuts import get_object_or_404

def index(request):

    products = Product.objects.all()[:10]
    return render(request, 'index.html', {'products': products})

def about(request):
    return render(request, 'about.html')

def error_404(request, exception):
    return render(request, '404.html', status=404)

def detailRestaurant(request):

    if request.method == "POST":
        return render(request, 'order.html')

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



def extra_pages(request, page_name):
    content_dict = {
        'about': {
            'page_title': 'HAKKIMIZDA',
            'page_content': '2017 yılında iki girişimci arkadaşın mutfak sevdalıları için kurduğu Mutfağınızın Yıldızı, kısa sürede ülkenin en sevilen yemek sipariş platformlarından biri haline geldi. Amacımız, lezzetli yemeklerin kapınıza kadar ulaşmasını sağlamakla kalmayıp, hem sizin için hem de iş ortaklarımız için eşsiz bir deneyim yaratmaktır. ',
            'page_content2': 'Sadece bir tıklamayla, yerel restoranlardan ulusal markalara kadar geniş bir yelpazede mutfağın eşsiz lezzetlerini keşfetme fırsatı sunuyoruz. Güvenli, hızlı ve kolay sipariş süreciyle lezzetin adımlarını sizlere getiriyoruz.',
            'page_content3': 'Sürdürülebilir bir büyüme ve adil bir ekosistem yaratma hedefimizle, tüm paydaşlarımızın memnuniyetini ön planda tutuyoruz. Siz de bu büyük ailenin bir parçası olun, lezzetin tadını birlikte çıkaralım!   ',
            'page_image': {'url': '', 'alt': ''}
        },
        'privacy': {
            'page_title': 'GİZLİLİK',
            'page_content': 'Biz, TencereKapak, kullanıcılarımızın gizliliğine büyük değer veririz. Web sitemizi ziyaret ettiğinizde veya servislerimizi kullandığınızda topladığımız kişisel veriler, sadece hizmetlerimizi size sunmak, kullanıcı deneyimini geliştirmek ve yasal yükümlülükleri yerine getirmek amacıyla kullanılır. Bu verilere, adınız, e-posta adresiniz, telefon numaranız ve ödeme bilgileriniz dahil olabilir. Verileriniz, üçüncü taraflarla kesinlikle paylaşılmaz veya satılmaz.',
            'page_image': {'url': '', 'alt': ''}
        },
        'termsconditions': {
            'page_title': 'ŞARTLAR & KOŞULLAR',
            'subtitle': '1. Kabul:',            
            'page_content': 'TencereKapak web sitesini kullanarak veya hizmetlerimizi satın alarak, bu şartlar ve koşulları kabul etmiş sayılırsınız. Eğer bu şartlar ve koşullarla ilgili bir anlaşmazlık yaşarsanız, lütfen hizmetlerimizi kullanmayın veya web sitemizi ziyaret etmeyin.',
            'subtitle2': '2. Hizmetler:',
            'page_content2': 'TencereKapak, web sitesinde listelenen hizmetleri sunmaktadır. Hizmetlerimizin sürekli kullanılabilirliği veya kesintisiz olacağı konusunda herhangi bir garanti vermemekteyiz. Ayrıca, hizmetlerimizi veya web sitemizi, önceden bildirimde bulunmaksızın herhangi bir zamanda değiştirme hakkımızı saklı tutarız.',                       
            'page_image': {'url': '', 'alt': ''}
        },
        'contacts': {
            'page_title': 'İLETİŞİM',
            'page_content': 'Beni Ara: +90 216-23-221',
            'page_image': {'url': 'https://img.fruugo.com/product/0/26/720275260_max.jpg', 'alt': 'telefon'}
        }
    }
    
    content = content_dict.get(page_name, {'page_title': 'Nau nau', 'page_content': 'Yok ki öyle bi sayfa', 'page_image': {'url': '', 'alt': ''}})

    return render(request, 'extra-pages.html', content)


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

def notfound(request):
    return render(request, '404.html')
