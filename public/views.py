from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .serializers import *
from rest_framework.views import APIView
from django.http import Http404

from shop.models import Shop, Domain

import os
from dotenv import load_dotenv
load_dotenv()

# Create your views here.

def getShopFromHost(host):
    try:
        if os.getenv('SHOP_ROOT_DOMAIN') in host:
            host = host.replace(os.getenv('SHOP_ROOT_DOMAIN'), '')
            return Shop.objects.get(slug=host)
        else:
            domain = Domain.objects.get(domain=host)
            return domain.shop
    except:
        raise Http404

class ShopDetailView(APIView):
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = []

    def get_object(self, host):
        return getShopFromHost(host)

    def get(self, request, host):
        shop = self.get_object(host)
        serialized_shop = ShopSerializer(shop)
        return Response(serialized_shop.data)


class ProductListView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = []

    def get(self, request, host):
        shop = getShopFromHost(host)
        products = shop.products.all()
        serialized_products = ProductListSerializer(products, many=True)
        return Response(serialized_products.data)
    
