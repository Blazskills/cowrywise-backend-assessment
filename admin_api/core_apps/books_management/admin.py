from django.contrib import admin

from core_apps.books_management.models import AdminAction, Book

# Register your models here.


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publisher', 'category', 'is_available']
    search_fields = ['title', 'author', 'category']


@admin.register(AdminAction)
class AdminActionAdmin(admin.ModelAdmin):
    list_display = ['action_type', 'book', 'action_date']
    search_fields = ['action_type']
