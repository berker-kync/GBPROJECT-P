from django.shortcuts import render

def panel(request):
    return render(request, 'restaurants-panel.html')
