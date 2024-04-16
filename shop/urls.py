#shop/urls.py
from django.urls import path, include

from .views import *

urlpatterns = [
    path('', ShopListView.as_view(), name='shop-list'),
    path('create/', ShopCreateView.as_view(), name='shop-create'),
    path('<str:slug>/', ShopDetailView.as_view(), name='shop-detail'),
    path('', include('product.urls')),
    
    
]
