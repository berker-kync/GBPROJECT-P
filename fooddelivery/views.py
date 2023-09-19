from django.shortcuts import render, redirect



def index(request):
    return render(request, 'index.html')

def submitrestaurant(request):
    return render(request, 'submit-restaurant.html')

def detailRestaurant(request):
    return render(request, 'detail-restaurant.html')








