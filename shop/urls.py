#shop/urls.py
from django.urls import path

from .views import *

urlpatterns = [
    path('', ShopListView.as_view(), name='shop-list'),
    path('create/', ShopCreateView.as_view(), name='shop-create'),
    path('<int:pk>/', ShopDetailView.as_view(), name='shop-detail'),
    
    
]
