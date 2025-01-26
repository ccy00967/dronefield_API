from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import ExterminatorLicense, Drone
from .serializers import ExterminatorLicenseSerializer, DroneSerializer
from .permissions import IsOwner
from user.models import CustomUser
from rest_framework.views import APIView
from django.http import Http404
from django.http import FileResponse


class ExterminatorLicenseImageView(APIView):
    """
    GET /exterminator-license/<uuid>/image/<image_type>/ -> 보호된 이미지 조회
    """
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get(self, request, uuid, image_type, format=None):
        # 요청한 사용자가 소유자인지 확인
        license = get_object_or_404(ExterminatorLicense, uuid=uuid, owner=request.user)

        # 제공할 이미지 타입 결정
        if image_type == 'license_image':
            file = license.license_image
        elif image_type == 'business_registration_image':
            file = license.business_registration_image
        else:
            return Response({"detail": "유효하지 않은 이미지 타입입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        if not file:
            raise Http404("이미지를 찾을 수 없습니다.")

        # 파일 제공
        return FileResponse(file.open(), content_type='image/jpeg')  # 필요에 따라 content_type 조정
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
class ExterminatorLicenseDetailView(generics.RetrieveUpdateDestroyAPIView):
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
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "라이선스가 성공적으로 삭제되었습니다."},
            status=status.HTTP_200_OK
        )
        
class DroneCreateAPIView(generics.CreateAPIView):
    """
    POST /drone/  -> 드론 생성
    """
    name = "drone-create"
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        return super().perform_create(serializer)

class DroneListAPIView(generics.ListAPIView):
    """
    GET /drone/  -> 드론 목록 조회
    """
    name = "drone-list"
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
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

class DroneDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /drone/<uuid>/   -> 드론 조회
    PATCH /drone/<uuid>/ -> 드론 부분 수정
    PUT /drone/<uuid>/   -> 드론 전체 수정
    """
    name = "drone-detail"
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
    ]
    lookup_field = "uuid"
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "드론이 성공적으로 삭제되었습니다."},
            status=status.HTTP_200_OK
        )
        
class DroneImageView(APIView):
    """
    GET /drone/<uuid>/image/ -> 보호된 이미지 조회
    """
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    name = "drone-image"

    def get(self, request, uuid, format=None):
        # 요청한 사용자가 소유자인지 확인
        drone = get_object_or_404(Drone, uuid=uuid, owner=request.user)
        if not drone.image:
            raise Http404("이미지를 찾을 수 없습니다.")

        # 파일 제공
        return FileResponse(drone.image.open(), content_type='image/jpeg')  # 필요에 따라 content_type 조정