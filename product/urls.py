#shop/urls.py
from django.urls import path

from .views import *

urlpatterns = [
    path('<int:shop_id>/', ProductList.as_view(), name='product-list'),
    # path('<int:product_id>/', ProductDetail.as_view(), name='product-detail'),
    # path('<int:product_id>/images/', ProductImageList.as_view(), name='product-image-list'),
    # path('<int:product_id>/images/<int:image_id>/', ProductImageDetail.as_view(), name='product-image-detail'),
    # path('<int:product_id>/tags/', TagList.as_view(), name='tag-list'),
    # path('categories/', CategoryList.as_view(), name='category-list'),
    # path('categories/<int:category_id>/', CategoryDetail.as_view(), name='category-detail'),
    # path('categories/<int:category_id>/subcategories/', SubcategoryList.as_view(), name='subcategory-list'),
    # path('categories/<int:category_id>/subcategories/<int:subcategory_id>/', SubcategoryDetail.as_view(), name='subcategory-detail'),
    # path('<int:product_id>/tags/<int:tag_id>/', TagDetail.as_view(), name='tag-detail'),
]
