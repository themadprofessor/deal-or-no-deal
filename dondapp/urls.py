from django.urls import path
from dondapp import views

urlpatterns = [
    path('', views.HomeView.dispatch, name='home'),
    path('about/', views.AboutView.dispatch, name='about'),
    path('category/', views.CategoryView.dispatch, name='category'),
    path('login/', views.LoginView.dispatch, name='login'),
    path('failed/', views.FailedView.dispatch, name='failed'),
    path('vote/', views.VoteView, name='vote'),
]
