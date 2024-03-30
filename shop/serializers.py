from rest_framework import serializers
from user.models import User  # Assuming your User model is in 'user' app
from .models import Shop

class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']  # You can adjust fields as needed



class ShopListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ('id','slug', 'name', 'description', 'logo',)



class ShopSerializer(serializers.ModelSerializer):
    managers = ManagerSerializer(many=True, read_only=True)
    owner = ManagerSerializer(read_only=True)
    class Meta:
        model = Shop
        fields = ('id','slug', 'owner', 'name', 'description', 'logo', 'managers', 'is_active', 'created_at', 'updated_at')
