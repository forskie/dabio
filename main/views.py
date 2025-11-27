from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Product, Category


def product(request):
    products = Product.objects.filter(available=True)[:3]
    return render(request, 'main/products.html', {'products': products})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, 'main/detail.html', {'product': product})


def home(request):
    return render(request, 'main/home.html')

def about_us(request):
    return render(request, 'main/about_us.html')

def product_list(request, category_slug=None):
    page = request.GET.get('page', 1)
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    category = None

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    
    products = products.order_by('-created_at') 
    paginator = Paginator(products, 9)
    
    try:
        current_page = paginator.page(page)
    except PageNotAnInteger:
        current_page = paginator.page(1)
    except EmptyPage:
        current_page = paginator.page(paginator.num_pages)
    
    context = {
        'category': category,
        'categories': categories,
        'products': current_page, 
        'slug_url': category_slug,
    }
    
    return render(request, 'main/product/list.html', context)
