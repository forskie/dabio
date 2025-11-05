from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def product(request):
    products = Product.objects.filter(available=True)[:3]
    return render(request, 'main/products.html', {'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, 'main/detail.html', {'product': product})

def home(request):
    return render(request, 'main/home.html')


def product_list(request, category_slug = None):
    category =None
    categories = Category.objects.all()
    products = Product.objects.all()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 
                  'main/product/list.html',
                  {"category" : category,
                  "categories" : categories, 
                  "products" : products})
