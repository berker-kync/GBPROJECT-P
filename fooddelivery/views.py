from django.shortcuts import render, redirect
from .models import Product


def index(request):
    return render(request, 'index.html')

def submitrestaurant(request):
    return render(request, 'submit-restaurant.html')

def detailRestaurant(request):

    products = Product.objects.all()

    return render(request, 'detail-restaurant.html', {'products': products})

def deneme(request):

    products = Product.objects.all()

    return render(request, 'deneme.html', {'products': products})






