from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product, name='products'),
    path('catalog/', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('catalog/<slug:category_slug>/', views.product_list, name='product_list'),
]