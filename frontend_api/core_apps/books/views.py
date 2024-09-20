from .serializers import UserSerializer
from .models import BookUser
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
        users = BookUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    # Get a specific BookUser by ID (GET request)
    def get(self, request, pk):
        user = get_object_or_404(BookUser, id=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
