from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publisher', 'category', 'is_available']
