from django.urls import path, include
from dondapp.category import views

urlpatterns = [
    path('index.html', views.page, name="category"),
    path('<int:id>/', views.CategoryView.dispatch, name="cat_id"),
    path('', views.CategoryView.dispatch, name='cat_all'),
    path('<int:id>/deals', views.CategoryView.dispatch, {'deals': True}, name='cat_deals')
]
