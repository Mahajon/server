from django.db import models
from shop.models import Shop
from user.models import User


# Create your models here.

class Category(models.Model):
    slug = models.SlugField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='categories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_categories')
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name.lower().replace(' ', '-')
            if Category.objects.filter(slug__startswith=self.slug, shop=self.shop).count() > 0:
                self.slug = f'{self.slug}-{Category.objects.filter(slug=self.slug).count()}'
        super(Category, self).save(*args, **kwargs)
 

class Subcategory(models.Model):
    slug = models.SlugField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories', null=True, blank=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='subcategories')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_subcategories')
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name.lower().replace(' ', '-')
            if Subcategory.objects.filter(slug__startswith=self.slug, shop=self.shop).count() > 0:
                self.slug = f'{self.slug}-{Subcategory.objects.filter(slug=self.slug).count()}'
        super(Subcategory, self).save(*args, **kwargs)


class Tag(models.Model):
    slug = models.SlugField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='tags')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_tags')
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name.lower().replace(' ', '-')
            if Tag.objects.filter(slug__startswith=self.slug, shop=self.shop).count() > 0:
                self.slug = f'{self.slug}-{Tag.objects.filter(slug=self.slug).count()}'
        super(Tag, self).save(*args, **kwargs)
    

class Product(models.Model):
    slug = models.SlugField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='products')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_products')
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.stock == 0:
            self.available = False

        if self.id and self.variants.all().count() > 0:
            stock = 0
            for variant in self.variants.all():
                stock += variant.stock
            self.stock = stock
        super(Product, self).save(*args, **kwargs)
        if self.variants.all().count() == 0:
            ProductVariant.objects.create(product=self, name='Default', price=self.price, stock=self.stock)
        
    

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.URLField()
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.stock == 0:
            self.available = False
        super(ProductVariant, self).save(*args, **kwargs)
    

class ProductImage(models.Model):
    image = models.URLField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.product.name
    

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    review = models.TextField()
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.product.name
    

