from utils.pagination import LargeResultsSetPagination, LargestResultsSetPagination
from .serializers import BookSerializer, UserSerializer
from .models import Book, BookUser
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.


class HealthCheck(APIView):
    def get(self, request):
        data = {"status": "Frontend Server is working !!!", "code": 200}
        return Response(data)


class UserCreateView(APIView):
    # Create a new BookUser (POST request)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # List all BookUsers (GET request)
    def get(self, request):
        users = BookUser.objects.all().order_by("id")
        paginator = LargeResultsSetPagination()
        paginated_user = paginator.paginate_queryset(users, request)
        serializer = UserSerializer(paginated_user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    # Get a specific BookUser by ID (GET request)
    def get(self, request, pk):
        user = get_object_or_404(BookUser, id=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookListAPIView(APIView):
    """
    Handles GET request to list all books.
    """

    def get(self, request):
        # Get all the books from the database
        books = Book.objects.all().order_by("id")
        paginator = LargeResultsSetPagination()
        paginated_book = paginator.paginate_queryset(books, request)
        serializer = BookSerializer(paginated_book, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BookDetailView(APIView):
    # Get a specific Book by ID (GET request)
    def get(self, request, pk):
        book = get_object_or_404(Book, id=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)
