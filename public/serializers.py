from rest_framework import serializers
from shop.models import Shop, Domain
from product.models import ProductImage, Product, ProductReview, ProductVariant


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ('id', 'domain', 'shop')


class ShopSerializer(serializers.ModelSerializer):
    domains = DomainSerializer(many=True, read_only=True)
    class Meta:
        model = Shop
        fields = ('id','slug', 'name', 'description', 'logo', 'domains', 'is_active')


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'product',)

class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = ('id', 'product', 'review', 'rating', 'created_at', 'updated_at')

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ('id', 'product', 'name', 'price', 'created_at', 'updated_at')

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    reviews = ProductReviewSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ('id', 'slug', 'shop', 'name', 'description', 'price', 'images', 'reviews', 'variants', 'created_at', 'updated_at')


class ProductListSerializer(serializers.ModelSerializer):
    #only the first image
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('id','slug', 'shop', 'name', 'image', 'description', 'price', 'image', 'created_at', 'updated_at')

    def get_image(self, obj):
        if obj.images.count() > 0:
           return obj.images.first().id
        else:
            None