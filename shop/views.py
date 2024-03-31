from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import Http404

from .permissions import IsShopOwnerOrManager
from .models import Shop
from .serializers import ShopSerializer, ShopListSerializer



class ShopPagination(PageNumberPagination):
    page_size = 10  # Set your desired page size


class ShopCreateView(generics.CreateAPIView):
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ShopListView(generics.ListAPIView):
    serializer_class = ShopListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        owner_shops = Shop.objects.filter(owner=user)
        managed_shops = user.managed_shops.all()
        return owner_shops.union(managed_shops)
    

class ShopDetailView(APIView):
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticated, IsShopOwnerOrManager]

    def get_object(self, slug):
        try:
            return Shop.objects.get(slug=slug)
        except Shop.DoesNotExist:
            raise Http404

    def get(self, request, slug):
        shop = self.get_object(slug)
        serialized_shop = ShopSerializer(shop)
        return Response(serialized_shop.data)


    def put(self, request, slug):
        shop = self.get_object(slug)
        self.check_object_permissions(request, shop)
        serialized_shop = ShopSerializer(shop, data=request.data, partial=True)
        if serialized_shop.is_valid(raise_exception=True):
            serialized_shop.save(update=True)
            return Response(serialized_shop.data, status=status.HTTP_200_OK)
        return Response(serialized_shop.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, slug):
        shop = self.get_object(slug)
        self.check_object_permissions(request, shop)
        shop.delete()
        return Response(status=status.HTTP_200_OK)
