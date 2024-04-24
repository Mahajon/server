from .models import *
from user.models import User
from shop.models import Shop
from rest_framework import serializers

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True, read_only=True)
    shop = serializers.SlugRelatedField(slug_field='slug', queryset=Shop.objects.all())
    class Meta:
        model = Category
        fields = '__all__'



class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True,read_only=True)
    slug = serializers.CharField()
    shop = serializers.SlugRelatedField(slug_field='slug', queryset=Shop.objects.all())
    def validate_slug(self, value):
        num_objs = Product.objects.filter(slug__startswith=value).count()
        if num_objs > 0:
            return f'{value}-{num_objs}'
        return value

    class Meta:
        model = Product
        fields = '__all__'


class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = '__all__'