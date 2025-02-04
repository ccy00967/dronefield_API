from rest_framework import viewsets
from .models import Notice, Alarm
from .serializers import NoticeSerializer, AlarmSerializer
from common.utils.pageanation import CustomPagination
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import render

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
    

import requests
from django.http import JsonResponse
from django.views.decorators.http import require_GET

@require_GET
def get_polygon_api(request):
    # GET 파라미터에서 x, y 좌표 받기
    x = request.GET.get('x')
    y = request.GET.get('y')
    if not (x and y):
        return JsonResponse({'error': 'x와 y 파라미터가 필요합니다.'}, status=400)

    # API KEY 설정 (실제 키로 교체하세요)
    KEY = '6C934ED4-5978-324D-B7DE-AC3A0DDC3B38'
    base_url = "https://api.vworld.kr/req/data"

    # API 호출에 필요한 파라미터 설정
    params = {
        "key": KEY,
        "request": "GetFeature",
        "data": "LP_PA_CBND_BUBUN",
        "geomFilter": f"POINT({x} {y})",
    }

    try:
        # vworld API에 GET 요청
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # HTTP 에러 발생 시 예외 발생

        # JSON 응답 파싱 (vworld API가 JSONP를 반환하는 경우, 별도 처리 필요할 수 있음)
        result = response.json()

        # polygon 좌표 추출 (응답 구조에 따라 키가 달라질 수 있음)
        polygon = result["response"]["result"]["featureCollection"]["features"][0]["geometry"]["coordinates"][0]

        return JsonResponse({"polygon": polygon})
    except Exception as e:
        # 에러 발생 시 에러 메시지 반환
        return JsonResponse({"error": str(e)}, status=500)

def get_naver_map(request):
    return render(request, 'naver_map.html')