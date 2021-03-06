from django.urls import path, include
from dondapp import views

urlpatterns = [
    path('', views.HomeView.dispatch, name='home'),
    path('about/', views.AboutView.dispatch, name='about'),
    path('category/', include('dondapp.category.urls')),
    path('login/', views.LoginView.dispatch, name='login'),
    path('failed/', views.FailedView.dispatch, name='failed'),
    path('vote/', views.VoteView.dispatch, name='vote'),
    path('deal/<int:id>/', views.DealView.dispatch, name='deal'),
    path('deal/', views.DealView.dispatch, name='deals'),
    path('search/', views.SearchView.dispatch, name='search'),
    path('user/', views.UserView.dispatch, name='user'),
    path('user/<str:username>/', views.UserView.dispatch, name='user_profile'),
    path('comment/', views.CommentView.dispatch, name='comment'),
    path('comment/<int:id>/', views.CommentView.dispatch, name='comment_id'),
    path('newdeals/', views.NewDealView.dispatch, name='new_deals'),
    path('topdeals/', views.TopDealView.dispatch, name='top_deals')
]
