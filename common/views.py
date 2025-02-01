from rest_framework import viewsets
from .models import Notice, Alarm
from .serializers import NoticeSerializer, AlarmSerializer
from common.utils.pageanation import CustomPagination
from rest_framework import generics, permissions, status
from rest_framework.response import Response

class NoticeCreateView(generics.CreateAPIView):
    """
    POST /notice/  -> 공지사항 생성
    """
    name = "notice-create"
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer

    def perform_create(self, serializer):
        serializer.save()
        return super().perform_create(serializer)

class NoticeListView(generics.ListAPIView):
    """
    GET /notice/  -> 공지사항 목록 조회
    """
    name = "notice-list"
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    pagination_class = CustomPagination
    
    def get_queryset(self):
        return super().get_queryset().order_by("-created_at")

class NoticeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /notice/<uuid>/  -> 공지사항 상세 조회
    PUT /notice/<uuid>/  -> 공지사항 수정
    DELETE /notice/<uuid>/  -> 공지사항 삭제
    """
    name = "notice-detail"
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    lookup_field = "uuid"
    
    def perform_update(self, serializer):
        return super().perform_update(serializer)
    
    def destroy(self, request, *args, **kwargs):
        return Response({"message": "공지사항이 성공적으로 삭제되었습니다."}, status=status.HTTP_200_OK)
    
    
class AlarmCreateView(generics.CreateAPIView):
    """
    POST /alarm/  -> 알람 생성
    """
    name = "alarm-create"
    queryset = Alarm.objects.all()
    serializer_class = AlarmSerializer
    
    def perform_create(self, serializer):
        serializer.save()
        return super().perform_create(serializer)

class AlarmListView(generics.ListAPIView):
    """
    GET /alarm/  -> 알람 목록 조회
    """
    name = "alarm-list"
    queryset = Alarm.objects.all()
    serializer_class = AlarmSerializer
    pagination_class = CustomPagination
    
    def get_queryset(self):
        return super().get_queryset().order_by("-created_at")
    
class AlarmDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /alarm/<uuid>/  -> 알람 상세 조회
    PUT /alarm/<uuid>/  -> 알람 수정
    DELETE /alarm/<uuid>/  -> 알람 삭제
    """
    name = "alarm-detail"
    queryset = Alarm.objects.all()
    serializer_class = AlarmSerializer
    lookup_field = "uuid"
    
    def perform_update(self, serializer):
        return super().perform_update(serializer)
    
    def destroy(self, request, *args, **kwargs):
        return Response({"message": "알림이 성공적으로 삭제되었습니다."}, status=status.HTTP_200_OK)