from rest_framework import serializers
from shop.models import Shop, Domain


class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = ('id', 'domain', 'shop')


class ShopSerializer(serializers.ModelSerializer):
    domains = DomainSerializer(many=True, read_only=True)
    class Meta:
        model = Shop
        fields = ('id','slug', 'name', 'description', 'logo', 'domains', 'is_active')
