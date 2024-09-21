from rest_framework import serializers
from .models import Book, BookUser, Borrow


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


class BorrowSerializer(serializers.ModelSerializer):
    # book_user = serializers.CharField(source="book_user.")
    book_user = serializers.SerializerMethodField()
    borrowed_on = serializers.SerializerMethodField()
    return_date = serializers.SerializerMethodField()
    book = serializers.CharField(source="book.title")

    class Meta:
        model = Borrow
        fields = ['id', 'book_user', 'book', 'borrowed_on', 'return_date']

    def get_borrowed_on(self, obj):
        return obj.borrowed_on.strftime("%m/%d/%Y, %H:%M:%S") if obj.borrowed_on else None

    def get_return_date(self, obj):
        return obj.return_date.strftime("%m/%d/%Y, %H:%M:%S") if obj.return_date else None

    def get_book_user(self, obj):
        return f"{obj.book_user.first_name} - {obj.book_user.last_name}" if obj.book_user else None
