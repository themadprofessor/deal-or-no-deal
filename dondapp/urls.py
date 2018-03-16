from django.urls import path
from dondapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('category/', views.category, name='category'),
    ]
