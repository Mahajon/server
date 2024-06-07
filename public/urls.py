#shop/urls.py
from django.urls import path, include

from .views import *

urlpatterns = [
    path('shop/<str:host>/', ShopDetailView.as_view(), name='shop-detail'),
    path('shop/<str:host>/products/', ProductListView.as_view(), name='shop-products-list'),
]
