from django.contrib import admin
from .models import Product, ProductImage

# Register your models here.


class productImageInline(admin.TabularInline):
    model = ProductImage
    readonly_fields = ['id']
    extra = 0

class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'slug']
    inlines = [productImageInline]

admin.site.register(Product, ProductAdmin)