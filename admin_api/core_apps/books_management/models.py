from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)


class AdminAction(models.Model):
    action_type = models.CharField(max_length=50)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    action_date = models.DateTimeField(auto_now_add=True)
