from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from shop.permissions import ShopPermission, ProductPermission
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import *
from .serializers import *
from .pagination import CustomPagination, NoPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView

class CategoryList(APIView):
    def get(self, request, shop_slug):
        categories = Category.objects.filter(shop__slug=shop_slug)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    def post(self, request, shop_slug):
        request.data['shop'] = Shop.objects.get(slug=shop_slug).id
        request.data['created_by'] = request.user.id
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CategoryDetail(APIView):
    def get(self, request, shop_slug, pk):
        category = Category.objects.get(shop=shop_slug, id=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    def put(self, request, shop_slug, pk):
        category = Category.objects.get(shop__slug=shop_slug, id=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, shop_slug, pk):
        category = Category.objects.get(shop__slug=shop_slug, id=pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, shop_slug, pk):
        category = Category.objects.get(shop__slug=shop_slug, id=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class SubcategoryList(APIView):
    def get(self, request, shop_slug, pk):
        subcategories = Subcategory.objects.filter(shop__slug=shop_slug, category=pk)
        serializer = SubcategorySerializer(subcategories, many=True)
        return Response(serializer.data)
    
    def post(self, request, shop_slug, pk):
        request.data['shop'] = Shop.objects.get(slug=shop_slug).id
        request.data['category'] = pk
        request.data['created_by'] = request.user.id
        serializer = SubcategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SubcategoryDetail(APIView):
    def get(self, request, shop_slug, pk, subpk):
        subcategory = Subcategory.objects.get(shop__slug=shop_slug, category=pk, id=subpk)
        serializer = SubcategorySerializer(subcategory)
        return Response(serializer.data)
    
    def put(self, request, shop_slug, pk, subpk):
        subcategory = Subcategory.objects.get(shop__slug=shop_slug, category=pk, id=subpk)
        serializer = SubcategorySerializer(subcategory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, shop_slug, pk, subpk):
        subcategory = Subcategory.objects.get(shop__slug=shop_slug, category=pk, id=subpk)
        serializer = SubcategorySerializer(subcategory, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, shop_slug, pk, subpk):
        subcategory = Subcategory.objects.get(shop__slug=shop_slug, category=pk, id=subpk)
        subcategory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class TagList(APIView):
    def get(self, request, shop_slug):
        tags = Tag.objects.filter(shop__slug=shop_slug)
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
    
    def post(self, request, shop_slug):
        request.data['shop'] = Shop.objects.get(slug=shop_slug).id
        request.data['created_by'] = request.user.id
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TagDetail(APIView):
    def get(self, request, shop_slug, tag_id):
        tag = Tag.objects.get(shop__slug=shop_slug, id=tag_id)
        serializer = TagSerializer(tag)
        return Response(serializer.data)
    
    def put(self, request, shop_slug, tag_id):
        tag = Tag.objects.get(shop__slug=shop_slug, id=tag_id)
        serializer = TagSerializer(tag, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, shop_slug, tag_id):
        tag = Tag.objects.get(shop__slug=shop_slug, id=tag_id)
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class ProductList(ListCreateAPIView):
    permission_classes = [IsAuthenticated, ProductPermission]
    pagination_class = CustomPagination
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'tags__name']

    def get_queryset(self):
        shop_slug = self.kwargs['shop_slug']
        return Product.objects.filter(shop__slug=shop_slug)

    def perform_create(self, serializer):
        shop_slug = self.kwargs['shop_slug']
        serializer.save(created_by=self.request.user, shop=Shop.objects.get(slug=shop_slug))





class ProductDetail(APIView):
    permission_classes = [IsAuthenticated, ProductPermission]
    def get(self, request, shop_slug, pk):
        product = Product.objects.get(shop__slug=shop_slug, id=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def put(self, request, shop_slug, pk):
        product = Product.objects.get(shop__slug=shop_slug, id=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, shop_slug, pk):
        product = Product.objects.get(shop__slug=shop_slug, id=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, shop_slug, pk):
        product = Product.objects.get(shop__slug=shop_slug, id=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductImageList(APIView):
    permission_classes = [IsAuthenticated, ProductPermission]
    def get(self, request, shop_slug, pk):
        images = ProductImage.objects.filter(product__shop__slug=shop_slug, product=pk)
        serializer = ProductImageSerializer(images, many=True)
        return Response(serializer.data)
    
    def post(self, request, shop_slug, pk):
        request.data['product'] = pk
        serializer = ProductImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProductImageDetail(APIView):
    permission_classes = [IsAuthenticated, ProductPermission]
    def get(self, request, shop_slug, pk, imgpk):
        image = ProductImage.objects.get(product__shop__slug=shop_slug, product=pk, id=imgpk)
        serializer = ProductImageSerializer(image)
        return Response(serializer.data)
    
    def put(self, request, shop_slug, pk, imgpk):
        image = ProductImage.objects.get(product__shop__slug=shop_slug, product=pk, id=imgpk)
        serializer = ProductImageSerializer(image, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, shop_slug, pk, imgpk):
        image = ProductImage.objects.get(product__shop__slug=shop_slug, product=pk, id=imgpk)
        serializer = ProductImageSerializer(image, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, shop_slug, pk, imgpk):
        image = ProductImage.objects.get(product__shop__slug=shop_slug, product=pk, id=imgpk)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)