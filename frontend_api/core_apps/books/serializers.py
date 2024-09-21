from rest_framework import serializers
from .models import Book, BookUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookUser
        fields = ['id', 'email', 'first_name', 'last_name', 'user_type']

    # Add a custom validation for the email field to ensure uniqueness
    def validate_email(self, value):
        if BookUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publisher', 'category', 'is_available']
