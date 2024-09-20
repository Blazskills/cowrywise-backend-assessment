from rest_framework.decorators import APIView
from rest_framework.response import Response

# Create your views here.


class HealthCheck(APIView):
    def get(self, request):
        data = {"status": "Server is working !!!", "code": 200}
        return Response(data)
