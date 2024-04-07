from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from shop.permissions import ShopProductPermission
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator

from .models import *
from .serializers import *
from .pagination import CustomPagination, NoPagination


class CategoryList(APIView):
    def get(self, request, shop_id):
        categories = Category.objects.filter(shop=shop_id)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    def post(self, request, shop_id):
        request.data['shop'] = shop_id
        request.data['created_by'] = request.user.id
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CategoryDetail(APIView):
    def get(self, request, shop_id, category_id):
        category = Category.objects.get(shop=shop_id, id=category_id)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    def put(self, request, shop_id, category_id):
        category = Category.objects.get(shop=shop_id, id=category_id)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, shop_id, category_id):
        category = Category.objects.get(shop=shop_id, id=category_id)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class SubcategoryList(APIView):
    def get(self, request, shop_id, category_id):
        subcategories = Subcategory.objects.filter(shop=shop_id, category=category_id)
        serializer = SubcategorySerializer(subcategories, many=True)
        return Response(serializer.data)
    
    def post(self, request, shop_id, category_id):
        request.data['shop'] = shop_id
        request.data['category'] = category_id
        request.data['created_by'] = request.user.id
        serializer = SubcategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SubcategoryDetail(APIView):
    def get(self, request, shop_id, category_id, subcategory_id):
        subcategory = Subcategory.objects.get(shop=shop_id, category=category_id, id=subcategory_id)
        serializer = SubcategorySerializer(subcategory)
        return Response(serializer.data)
    
    def put(self, request, shop_id, category_id, subcategory_id):
        subcategory = Subcategory.objects.get(shop=shop_id, category=category_id, id=subcategory_id)
        serializer = SubcategorySerializer(subcategory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, shop_id, category_id, subcategory_id):
        subcategory = Subcategory.objects.get(shop=shop_id, category=category_id, id=subcategory_id)
        subcategory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class TagList(APIView):
    def get(self, request, shop_id):
        tags = Tag.objects.filter(shop=shop_id)
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
    
    def post(self, request, shop_id):
        request.data['shop'] = shop_id
        request.data['created_by'] = request.user.id
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TagDetail(APIView):
    def get(self, request, shop_id, tag_id):
        tag = Tag.objects.get(shop=shop_id, id=tag_id)
        serializer = TagSerializer(tag)
        return Response(serializer.data)
    
    def put(self, request, shop_id, tag_id):
        tag = Tag.objects.get(shop=shop_id, id=tag_id)
        serializer = TagSerializer(tag, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, shop_id, tag_id):
        tag = Tag.objects.get(shop=shop_id, id=tag_id)
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




class ProductList(APIView):
    permission_classes = [IsAuthenticated, ShopProductPermission]
    # get product List with pagination and custom per page
    # pagination_class = CustomPagination
    pagination_class = NoPagination
    def get(self, request, shop_id):
        products = Product.objects.filter(shop=shop_id).order_by('-created_at')
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


    # create product
    def post(self, request, shop_id):
        _mutable = request.data._mutable
        request.data._mutable = True
        request.data['created_by'] = request.user.id
        if not request.data['shop']:
            request.data['shop'] = shop_id
        request.data._mutable = _mutable
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProductDetail(APIView):
    def get(self, request, shop_id, product_id):
        product = Product.objects.get(shop=shop_id, id=product_id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def put(self, request, shop_id, product_id):
        product = Product.objects.get(shop=shop_id, id=product_id)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, shop_id, product_id):
        product = Product.objects.get(shop=shop_id, id=product_id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class ProductImageList(APIView):
    def get(self, request, shop_id, product_id):
        images = ProductImage.objects.filter(product=product_id)
        serializer = ProductImageSerializer(images, many=True)
        return Response(serializer.data)
    
    def post(self, request, shop_id, product_id):
        request.data['product'] = product_id
        serializer = ProductImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProductImageDetail(APIView):
    def get(self, request, shop_id, product_id, image_id):
        image = ProductImage.objects.get(product=product_id, id=image_id)
        serializer = ProductImageSerializer(image)
        return Response(serializer.data)
    
    def put(self, request, shop_id, product_id, image_id):
        image = ProductImage.objects.get(product=product_id, id=image_id)
        serializer = ProductImageSerializer(image, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, shop_id, product_id, image_id):
        image = ProductImage.objects.get(product=product_id, id=image_id)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    