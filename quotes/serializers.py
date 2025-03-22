from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Quote

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ['id', 'text', 'author', 'category', 'created_at', 'theme', 'views', 'shares', 'rating']
        read_only_fields = ['created_at']
