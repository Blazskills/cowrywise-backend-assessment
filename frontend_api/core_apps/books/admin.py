from django.contrib import admin
from .models import Book, BookUser


@admin.register(BookUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'user_type']
    search_fields = ['email', 'first_name', 'last_name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publisher', 'category', 'is_available']
    search_fields = ['title', 'author', 'category']
