#shop/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *

# router = DefaultRouter()

# router.register('<int:shop>/categories', CategoryView, basename='category')
# router.register('<int:shop>/products', ProductView, basename='product')
# router.register('subcategories', SubcategoryView, basename='subcategory')

urlpatterns = [
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category-detail'),
    path('categories/<int:pk>/subcategories/', SubcategoryList.as_view(), name='subcategory-list'),
    path('categories/<int:pk>/subcategories/<int:subpk>/', SubcategoryDetail.as_view(), name='subcategory-detail'),
    path('products/', ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('products/<int:pk>/images/', ProductImageList.as_view(), name='product-image-list'),
    path('products/<int:pk>/images/<int:imagepk>/', ProductImageDetail.as_view(), name='product-image-detail'),

]

# urlpatterns += router.urls
