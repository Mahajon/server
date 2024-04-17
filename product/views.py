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
    def get(self, request):
        shop = request.query_params.get('shop')
        categories = Category.objects.filter(shop__slug=shop)
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    def post(self, request, ):
        request.data['created_by'] = request.user.id
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CategoryDetail(APIView):
    def get(self, request, pk):
        category = Category.objects.get( id=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    
    def put(self, request, pk):
        category = Category.objects.get(id=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        category = Category.objects.get(id=pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        category = Category.objects.get(id=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class SubcategoryList(APIView):
    def get(self, request, pk):
        subcategories = Subcategory.objects.filter(category=pk)
        serializer = SubcategorySerializer(subcategories, many=True)
        return Response(serializer.data)
    
    def post(self, request, pk):
        request.data['category'] = pk
        request.data['created_by'] = request.user.id
        serializer = SubcategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SubcategoryDetail(APIView):
    def get(self, request, pk, subpk):
        subcategory = Subcategory.objects.get(category=pk, id=subpk)
        serializer = SubcategorySerializer(subcategory)
        return Response(serializer.data)
    
    def put(self, request, pk, subpk):
        subcategory = Subcategory.objects.get(category=pk, id=subpk)
        serializer = SubcategorySerializer(subcategory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk, subpk):
        subcategory = Subcategory.objects.get(category=pk, id=subpk)
        serializer = SubcategorySerializer(subcategory, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, subpk):
        subcategory = Subcategory.objects.get(category=pk, id=subpk)
        subcategory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class TagList(APIView):
    def get(self, request):
        shop = request.query_params.get('shop')
        tags = Tag.objects.filter(shop__slug=shop)
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        request.data['created_by'] = request.user.id
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TagDetail(APIView):
    def get(self, request, tag_id):
        tag = Tag.objects.get(id=tag_id)
        serializer = TagSerializer(tag)
        return Response(serializer.data)
    
    def put(self, request, tag_id):
        tag = Tag.objects.get(id=tag_id)
        serializer = TagSerializer(tag, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, tag_id):
        tag = Tag.objects.get(id=tag_id)
        tag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


class ProductList(ListCreateAPIView):
    permission_classes = [IsAuthenticated, ProductPermission]
    pagination_class = CustomPagination
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'tags__name']
    ordering_fields = ['id','name', 'price', 'created_at']
    # default ordering
    ordering = ['-id']

    def get_queryset(self):
        #extract the shop slug from get params
        shop_slug = self.request.query_params.get('shop')
        return Product.objects.filter(shop__slug=shop_slug)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)





class ProductDetail(APIView):
    permission_classes = [IsAuthenticated, ProductPermission]
    def get(self, request, pk):
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    def put(self, request, pk):
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        product = Product.objects.get(id=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductImageList(APIView):
    permission_classes = [IsAuthenticated, ProductPermission]
    def get(self, request, pk):
        images = ProductImage.objects.filter(product__product=pk)
        serializer = ProductImageSerializer(images, many=True)
        return Response(serializer.data)
    
    def post(self, request, pk):
        request.data['product'] = pk
        serializer = ProductImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProductImageDetail(APIView):
    permission_classes = [IsAuthenticated, ProductPermission]
    def get(self, request, pk, imgpk):
        image = ProductImage.objects.get(product__product=pk, id=imgpk)
        serializer = ProductImageSerializer(image)
        return Response(serializer.data)
    
    def put(self, request, pk, imgpk):
        image = ProductImage.objects.get(product__product=pk, id=imgpk)
        serializer = ProductImageSerializer(image, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk, imgpk):
        image = ProductImage.objects.get(product__product=pk, id=imgpk)
        serializer = ProductImageSerializer(image, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, imgpk):
        image = ProductImage.objects.get(product__product=pk, id=imgpk)
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)