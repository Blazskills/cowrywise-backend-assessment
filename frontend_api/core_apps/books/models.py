from django.db import models


class BookUser(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user_type = models.CharField(
        max_length=20,
        choices=[("Admin", "Admin"), ("Non-Admin", "Non-Admin")],
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user_type})"


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} by {self.author} (Publisher: {self.publisher})"


class Borrow(models.Model):
    book_user = models.ForeignKey(BookUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_on = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField()

    def __str__(self):
        return f"{self.book_user.first_name} {self.book_user.last_name} borrowed '{self.book.title}' on {self.borrowed_on.strftime('%Y-%m-%d')}"
