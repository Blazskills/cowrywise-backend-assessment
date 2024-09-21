from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class LargestResultsSetPagination(PageNumberPagination):
    page_size = 100000
    page_size_query_param = 'page_size'
    max_page_size = 500000


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 5000


class SmallResultsSetPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000


class TinyResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class TiniestResultsSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 5


# from rest_framework.pagination import PageNumberPagination


class CustomPagination(LargeResultsSetPagination):
    LargeResultsSetPagination

    def get_paginated_response(self, data):
        return Response({
            'data': data,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'page_size': self.page_size,
        })
