from rest_framework.decorators import APIView
from rest_framework.response import Response


from rest_framework import status
from django.shortcuts import get_object_or_404

from core_apps.books_management.models import Book
from core_apps.books_management.producer import send_book_message
from core_apps.books_management.serializers import BookSerializer

# Create your views here.


class HealthCheck(APIView):
    def get(self, request):
        data = {"status": "Server is working !!!", "code": 200}
        return Response(data)


class BookListCreateView(APIView):
    """
    Handles GET (list all books) and POST (create a new book) requests.
    """

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            book = serializer.save()

            book_data = {
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'publisher': book.publisher,
                'category': book.category,
                'is_available': book.is_available,
            }
            send_book_message("book_queue", book_data)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailView(APIView):
    """
    Handles GET, PUT, and DELETE requests for a single book.
    """

    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            send_book_message("book_queue_update", serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        send_book_message("book_queue_delete", {"id": pk})
        return Response(status=status.HTTP_204_NO_CONTENT)
