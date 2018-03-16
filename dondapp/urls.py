from django.urls import path, re_path
from dondapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('category/', views.category, name='category'),
    path('login/', views.login, name='login'),
    path('failed/', views.failed, name='failed'),
    path('logout/', views.logout, name='logout'),
    path('vote/', views.vote, name='vote_post'),
    re_path(r'^vote/(?P<deal_id>\d)/$', views.vote_get, name='vote_get')
    ]
