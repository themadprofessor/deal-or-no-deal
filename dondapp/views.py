from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    return render(request, 'dondapp/home.html')


def about(request):
    return render(request, 'dondapp/about.html')


def category(request):
    return render(request, 'dondapp/category.html')


def failed(request):
    return render(request, 'dondapp/failed.html')


def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        django_login(request, user)
        print("Successful login")
        return redirect("home")
    else:
        print("Failed login")
        return redirect("failed")


@login_required
def logout(request):
    django_logout(request)
    return redirect("home")
