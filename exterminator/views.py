from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import ExterminatorLicense
from .serializers import ExterminatorLicenseSerializer
from user.models import CustomUser


class ExterminatorLicenseCreateView(generics.CreateAPIView):
    """
    POST /exterminator-license/  -> 라이선스 생성
    """
    name = "exterminator-license-create"
    queryset = ExterminatorLicense.objects.all()
    serializer_class = ExterminatorLicenseSerializer
    permission_classes = [
        permissions.IsAuthenticated,         # 생성은 인증된 사용자만 가능
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        return super().perform_create(serializer)

class ExterminatorLicenseListView(generics.ListAPIView):
    """
    GET /exterminator-license/  -> 라이선스 목록 조회
    """
    name = "exterminator-license-list"
    queryset = ExterminatorLicense.objects.all()
    serializer_class = ExterminatorLicenseSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]

    def get_queryset(self):
        queryset = super().get_queryset()
        try:
            queryset = queryset.filter(owner=self.request.user)
        except TypeError:
            queryset = queryset.none()
        return queryset
class ExterminatorLicenseDetailView(generics.RetrieveUpdateAPIView):
    """
    GET /exterminator-license/<uuid>/   -> 라이선스 조회
    PATCH /exterminator-license/<uuid>/ -> 라이선스 부분 수정
    PUT /exterminator-license/<uuid>/   -> 라이선스 전체 수정
    """
    name = "exterminator-license-detail"
    queryset = ExterminatorLicense.objects.all()
    serializer_class = ExterminatorLicenseSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]
    lookup_field = "uuid"