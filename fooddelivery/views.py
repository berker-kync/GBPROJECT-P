from django.shortcuts import render, redirect
from .forms import RegisterForm


def index(request):
    return render(request, 'index.html')

def submitrestaurant(request):
    return render(request, 'submit-restaurant.html')








