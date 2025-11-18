from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
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
    page = request.GET.get('page', 1)
    category =None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        paginator = Paginator(products.filter(category=category), 1)
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        current_page = paginator.page(int(page))

    paginator = Paginator(products, 9)
    current_page = paginator.page(int(page))

    
    return render(request, 
                  'main/product/list.html',
                  {"category" : category,
                  "categories" : categories, 
                  "products" : current_page,
                  "slug_url" : category_slug})
