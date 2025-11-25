from django.db import models
from django.utils import timezone
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    

class Size(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name
    
class ProductSize(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='product_size')
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    stock =  models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.size.name} ({self.stock} in stock) for {self.product.name}"
    
    

    
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, 
                                related_name='products')
    color = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    descriptions = models.TextField(blank=True)
    main_image = models.ImageField(upload_to='products/main/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    discount = models.IntegerField(default=0, verbose_name='Скидка %')
    

    @property
    def sell_price(self):
        if self.discount > 0:
            return self.price - (self.price * self.discount / 100)
        return self.price
    
    @property
    def discounted_price(self):
        return self.sell_price
    
    @property
    def savings(self):
        if self.discount > 0:
            return self.price - self.sell_price
        return 0
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,
                                related_name='images')
    image = models.ImageField(upload_to='products/extra/')
    