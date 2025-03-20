from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Quote

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Hide password in response

    class Meta:
        model = User
        fields = ['id', 'username', 'password']  # Add 'id' to response

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ['id', 'text', 'author', 'category']