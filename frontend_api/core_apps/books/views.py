from utils.pagination import LargeResultsSetPagination
from .serializers import BookSerializer, BorrowSerializer, UserSerializer
from .models import Book, BookUser, Borrow
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
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


class BorrowBookAPIView(APIView):

    """
    Handles GET request to list all books.
    """

    def get(self, request):
        # Get all the books from the database
        borrowed_books = Borrow.objects.all().order_by("id")
        paginator = LargeResultsSetPagination()
        paginated_borrowed_book = paginator.paginate_queryset(borrowed_books, request)
        serializer = BorrowSerializer(paginated_borrowed_book, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    """
    Handles creating and updating borrowed books.
    """

    def post(self, request):
        email = request.data.get('email')
        book_id = request.data.get('book_id')
        if not email:
            return Response(
                {"message": "Email is required to borrow a book."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not book_id:
            return Response(
                {"message": "Book ID is required to borrow a book."},
                status=status.HTTP_400_BAD_REQUEST
            )

        book_user = get_object_or_404(BookUser, email=email)
        book = get_object_or_404(Book, pk=book_id)
        existing_borrow = Borrow.objects.filter(
            book_user=book_user,
            book=book,
            return_date__isnull=True
        ).exists()

        if existing_borrow:
            # Return a message indicating that the user has already borrowed the book
            return Response(
                {"message": f"Unable to borrow '{book.title}' because you have already borrowed it and not returned it."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # If the book is available, create a borrow record
        if book.is_available:
            borrow = Borrow.objects.create(
                book_user=book_user,
                book=book,
                return_date=None
            )

            # Mark the book as unavailable since it is now borrowed
            # The only reason that this will change to true is when the admin api send a response that the bok is available
            # Which mean more people can borrow the same book even when it has not been returned

            book.is_available = False
            book.save()

            serializer = BorrowSerializer(borrow)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # If the book is not available, return an error response
            return Response(
                {"message": f"'{book.title}' is currently unavailable for borrowing."},
                status=status.HTTP_400_BAD_REQUEST
            )

    def put(self, request, pk):
        borrow = get_object_or_404(Borrow, pk=pk)
        borrow.return_date = request.data.get('return_date', timezone.now())
        borrow.save()
        book = borrow.book
        book.is_available = True
        book.save()

        return Response({"message": "Book returned successfully"}, status=status.HTTP_200_OK)
