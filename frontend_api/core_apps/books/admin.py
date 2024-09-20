from django.contrib import admin
from .models import BookUser


@admin.register(BookUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'user_type']
    search_fields = ['email', 'first_name', 'last_name']
