from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.core.paginator import EmptyPage


class CustomPagination(PageNumberPagination):
    page_size = 10  # 기본 페이지 크기
    page_size_query_param = 'page_size'  # 요청에서 페이지 크기를 변경할 수 있는 파라미터
    page_size = 5  # 기본 페이지 크기
    page_size_query_param = (
        "page_size"  # 요청에서 페이지 크기를 변경할 수 있는 파라미터
    )
    max_page_size = 100  # 최대 페이지 크기 제한

    def paginate_queryset(self, queryset, request, view=None):
        try:
            return super().paginate_queryset(queryset, request, view)
        except EmptyPage:
            # 요청된 페이지가 없을 경우
            self.page = None
            return None

    def get_paginated_response(self, data):
        
        return Response({
            "total_items": self.page.paginator.count,
            "current_page": self.page.number,
            "page_size": self.page_size,
            "total_pages": self.page.paginator.num_pages,
            "has_next": self.page.has_next(),
            "has_previous": self.page.has_previous(),
            "data": data
        })