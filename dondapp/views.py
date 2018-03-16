from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseNotFound, HttpResponse
from django.views.decorators.http import require_http_methods
from dondapp import models
import json


# Create your views here.

@require_http_methods(['GET'])
def home(request):
    return render(request, 'dondapp/home.html')


@require_http_methods(['GET'])
def about(request):
    return render(request, 'dondapp/about.html')


@require_http_methods(['GET'])
def category(request):
    return render(request, 'dondapp/category.html')


@require_http_methods(['GET'])
def failed(request):
    return render(request, 'dondapp/failed.html')


@require_http_methods(['POST'])
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
@require_http_methods(['POST'])
def vote(request):
    deal_id = request.POST['deal']
    upvote = request.POST['upvote']
    deal = models.Deal.objects.get(deal_id=deal_id)
    if deal is not None:
        if upvote:
            deal.upvotes += 1
        else:
            deal.downvotes -= 1

        deal.save()
        return HttpResponse(status=200)
    else:
        return HttpResponseNotFound("Deal not found")


@require_http_methods(['GET'])
def vote_get(request):
    deal_id = request.GET.get("deal_id")
    if deal_id is not None:
        deal = models.Deal.objects.get(deal_id=deal_id)
        response_data = {
            'upvotes': deal.upvotes,
            'downvotes': deal.downvotes
        }
        return HttpResponse(json.dumps(response_data), status=200)
    else:
        return HttpResponseNotFound("Deal not found")


@login_required
def logout(request):
    django_logout(request)
    return redirect("home")

