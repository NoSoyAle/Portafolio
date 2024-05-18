from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'app/home.html')

def iniciosesion(request):
    return render(request, 'app/iniciosesion.html')

def crearcuenta(request):
    return render(request, 'app/crearcuenta.html')
