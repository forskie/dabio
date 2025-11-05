from django.urls import path
from main.views import product, product_detail, home
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('product', views.product, name='product'),
]