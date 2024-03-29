# example/urls.py
from django.urls import path

from .views import *


urlpatterns = [
    path('me/', UserViewSet.as_view({'get': 'get'})),
]