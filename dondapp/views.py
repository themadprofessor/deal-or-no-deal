from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'dondapp/home.html')

def about(request):
    return render(request, 'dondapp/about.html')

def category(request):
    return render(request, 'dondapp/category.html')

def login(request):
    return render(request, 'dondapp/login.html')
