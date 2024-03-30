#user/serializers.py
from rest_framework import serializers
from .models import User, Provider


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ['name', 'created_at']



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    providers = ProviderSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'uid', 'email', 'password', 'picture', 'first_name', 'last_name', 'providers']
        def create(self, validated_data):
            password = validated_data.pop('password', None)
            instance = self.Meta.model(**validated_data)
            if password is not None:
                instance.set_password(password)
                instance.save()
            return instance
        def update(self, instance, validated_data):
            password = validated_data.pop("password", None)
            for attr, value in validated_data.items():
                setattr(instance, attr, value)
            if password is not None:
                instance.set_password(password)
                instance.save()
            return instance