import json
from farmer.models import FarmInfo
from django.views.decorators.http import require_GET
from django.http import JsonResponse
import requests
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


@require_GET
def naver_map_view(request, uuid):

    farminfo = FarmInfo.objects.get(uuid=uuid)

    farminfo_jibun = farminfo.jibun

    adrass = farminfo_jibun
    normalized_address = ' '.join(adrass.split())

    # VWorld API 키 및 기본 URL 설정
    vworld_key = "C5DD4C9E-0189-3CBF-8AFA-7BE8B0D09DF6"
    baseurl_search = "https://api.vworld.kr/req/search"

    parms_search = {
        "key": vworld_key,
        "request": "search",
        "query": normalized_address,
        "type": "address",
        "category": "parcel",
        "format": "json"
    }

    try:
        response = requests.get(baseurl_search, params=parms_search)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ValueError(f"API 요청 실패: {e}")

    response_json = response.json()
    print("=====================================")
    print(response_json)
    print("=====================================")
    item_x = response_json.get("response", {}).get("result", {}).get("items", [])[0].get("point", {}).get("x")
    item_y = response_json.get("response", {}).get("result", {}).get("items", [])[0].get("point", {}).get("y")

    # 첫 번째 API 요청 파라미터 설정
    baseurl_search = "https://api.vworld.kr/req/data"
    params_search = {
        "page": "1",
        "size": "1",
        "request": "GetFeature",
        "geomFilter": f"POINT({item_x} {item_y})",
        "data": "LP_PA_CBND_BUBUN",
        "format": "json",
        "key": vworld_key
    }

    try:
        # 첫 번째 API 요청 (주소 검색)
        response = requests.get(baseurl_search, params=params_search)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ValueError(f"API 요청 실패: {e}")

    response_json = response.json()
    items = []
    items = response_json.get("response", {}).get("result", {}).get(
        "featureCollection", {}).get("features", [])[0].get("geometry", {}).get("coordinates", [])[0]
    print(response_json)
    print(items)
    print("=====================================")
    transformed_coordinates = [[[lat, lon]
                                for lon, lat in path] for path in items]
    print(transformed_coordinates)
    polygon_paths = []
    polygon_paths = transformed_coordinates
    # polygon_paths = [
    #     [
    #         [35.147373835257326, 126.79203322494573],
    #         [35.14755604833613, 126.79258941275606],
    #         [35.147590671134544, 126.79277358828519],
    #         [35.14758075760663, 126.79277438176567],
    #         [35.147571260060865, 126.79283355570524],
    #         [35.14754233918198, 126.79287752536425],
    #         [35.14751096516151, 126.79279497146653],
    #         [35.14749401356581, 126.79274952766468],
    #         [35.14743830739503, 126.79260157637478],
    #         [35.14744565540955, 126.79260795541967],
    #         [35.14746926536196, 126.79258382922568],
    #         [35.14736357287228, 126.79225998384867],
    #         [35.147375703758726, 126.79226443017986],
    #         [35.147373140379585, 126.79225716101384],
    #         [35.1472841736161, 126.79200485653521],
    #         [35.14735572112381, 126.79202979260312],
    #         [35.147373835257326, 126.79203322494573]
    #     ]
    # ]

    context = {
        'naver_client_id': 'hmpfs1a6fl',
        'vworld_api_key': "6C934ED4-5978-324D-B7DE-AC3A0DDC3B38",
        "x": item_x,
        "y": item_y,
        "polygon_paths": json.dumps(polygon_paths)  # JSON 형식으로 변환
    }
    return render(request, 'naver_map.html', context)
