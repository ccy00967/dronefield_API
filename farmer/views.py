from rest_framework import generics
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from farmer.permissions import OnlyOwnerCanUpdate
import requests
from django.db.models.functions import Cast
from django.db.models import FloatField
from farmer.models import FarmInfo, FarmInfoImage
from farmer.serializers import FarmInfoSerializer
from farmer.serializers import FarmInfoUpdateSerializer
from farmer.serializers import FarmInfoBriefSerializer, FarmInfoImageSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from common.utils.pageanation import CustomPagination
from trade.models import Request
from rest_framework.exceptions import PermissionDenied
from rest_framework import viewsets
from django.shortcuts import render
from core.settings import CONSUMER_KEY, CONSUMER_SECRET

# 농지목록 조회
class FarmInfoListView(generics.ListAPIView):
    queryset = FarmInfo.objects.all()
    serializer_class = FarmInfoBriefSerializer
    name = "land_info_list"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        try:
            queryset = queryset.filter(owner=self.request.user)
        except TypeError:  
            raise PermissionDenied("로그인이 필요합니다.")
            
            queryset = queryset.none()

        if "owner" in self.request.query_params:
            owner_uuid = self.request.query_params.get("owner")
            queryset = queryset.filter(owner__uuid=owner_uuid)

        return queryset


class FarmInfoCreateView(generics.CreateAPIView):
    queryset = FarmInfo.objects.all()
    serializer_class = FarmInfoSerializer
    name = "land_info_create"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # 신청한 유저 정보를 함께 저장
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    def post(self, request, *args, **kwargs):
        vworld_key = "6C934ED4-5978-324D-B7DE-AC3A0DDC3B38"
        jibun = request.data.get("jibun")
        road = request.data.get("road")
        pnu = request.data.get("pnu")
        cd = request.data.get("cd")
        lndpclAr = request.data.get("lndpclAr")
        baseurl = "https://api.vworld.kr/req/search"
        response_pnu = requests.get(f"{baseurl}"
                                   +f"?page=1&size=1"
                                   +f"&request=search"
                                   +f"&query={jibun}"
                                   +f"&type=address"
                                   +f"&category=parcel"
                                   +f"&format=json"
                                   +f"&key={vworld_key}")
        
        response_pnu_result=response_pnu.json()["response"].get("result").get("items")[0].get("id")
        
        
        if response_pnu_result != pnu:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "cd값이 일치하지 않습니다."})
        
        baseurl = "https://api.vworld.kr/ned/data/ladfrlList"
        response_lndpclAr = requests.get(f"{baseurl}"
                                    +f"?domain=https://dronefield.co.kr"
                                    +f"&pnu={response_pnu_result}"
                                    +f"&format=json"
                                    +f"&key={vworld_key}")
        
        response_lndpclAr_result = response_lndpclAr.json()["ladfrlVOList"].get("ladfrlVOList")[0].get("lndpclAr")
        
        print(f"{pnu} : {response_pnu_result}")
        print(f"{lndpclAr} : {response_lndpclAr_result}")
        print(f"{cd} :  ")
        
        baseurl_sgisapi = "https://sgisapi.kostat.go.kr/OpenAPI3/auth/authentication.json"
        response_cd_access = requests.get(f"{baseurl_sgisapi}"
                                    +f"?consumer_key={CONSUMER_KEY}"
                                    +f"&consumer_secret={CONSUMER_SECRET}"
                                    ).json()["result"].get("accessToken")
        
        baseurl_sgisapi = "https://sgisapi.kostat.go.kr/OpenAPI3/addr/geocode.json"
        response_cd_result = requests.get(f"{baseurl_sgisapi}"
                                    +f"?accessToken={response_cd_access}"
                                    +f"&address={jibun}")
        response_cd_result = response_cd_result.json()["result"].get("resultdata")[0].get("ri_cd")
        print(response_cd_result)
        
        if  response_lndpclAr_result != lndpclAr:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "lndpclAr값이 일치하지 않습니다."})
        
        
        
       
        
        return super().post(request, *args, **kwargs)
        
        
    
        


# 농지 정보 조회, 수정, 삭제
class FarmInfoAPIView(generics.GenericAPIView):
    queryset = FarmInfo.objects.all()
    serializer_class = FarmInfoSerializer
    name = "land_info_update_delete"
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        OnlyOwnerCanUpdate,
    )
    
    
    def get_object(self, uuid):
        try:
            return FarmInfo.objects.get(uuid=uuid)
        except FarmInfo.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, uuid):
        farm_info = self.get_object(uuid)
        serializer = FarmInfoSerializer(farm_info)
        return Response(serializer.data)

    def patch(self, request, uuid):
        farm_info = self.get_object(uuid)
        serializer = FarmInfoUpdateSerializer(farm_info, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # 신청서에 등록된 농지는 삭제 불가능
    def delete(self, request, uuid):
        try:
            farm_info  = self.get_object(uuid)
            
            if Request.objects.filter(landInfo=farm_info).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "신청서에 등록된 농지는 삭제할 수 없습니다."})
            
            farm_info.delete()
            return Response(status=status.HTTP_204_NO_CONTENT, data={"message": "농지 정보가 삭제되었습니다."})
        except Exception as e:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": f"에러 발생: {e}"})

    

class TotalLandAreaAPIView(generics.GenericAPIView):
    queryset = FarmInfo.objects.all()
    serializer_class = FarmInfoSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 현재 사용자의 모든 땅 가져오기
        user_lands = FarmInfo.objects.filter(owner=request.user)

       # lndpclAr를 FloatField로 변환한 후 합산하고 None을 0으로 처리
        total_area = user_lands.aggregate(
            total_lndpclAr=Sum(Cast('lndpclAr', FloatField()), output_field=FloatField())
        )['total_lndpclAr'] or 0

        # 응답 데이터 직렬화 및 반환
        return Response({'total_lndpclAr': total_area})


class FarmInfoImageAPIView(generics.GenericAPIView):
    queryset = FarmInfoImage.objects.all()
    serializer_class = FarmInfoImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_farm(self, uuid):
        from rest_framework.exceptions import NotFound
        try:
            return FarmInfo.objects.get(uuid=uuid)
        except FarmInfo.DoesNotExist:
            raise NotFound("해당 농지 정보가 존재하지 않습니다.")

    def get_queryset(self):
        """해당 농지에 연결된 이미지들만 필터링"""
        farm_uuid = self.kwargs.get('uuid')
        return FarmInfoImage.objects.filter(land_info__uuid=farm_uuid)

    # 예: GET /land/<uuid>/image/ => 이미지 목록
    def get(self, request, uuid):
        images = self.get_queryset()
        serializer = self.get_serializer(images, many=True)
        return Response(serializer.data)

    # 예: POST /land/<uuid>/image/ => 이미지 새로 업로드
    def post(self, request, uuid):
        farm_info = self.get_farm(uuid)
        image_file = request.FILES.get('image')  # 단일 업로드 예시
        
        if not image_file:
            return Response({"detail": "이미지 파일이 필요합니다."},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            new_image = FarmInfoImage.objects.create(farm_info=farm_info, image=image_file)
            serializer = FarmInfoImageSerializer(new_image)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"detail": f"이미지 업로드 실패: {e}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 예: DELETE /land/<uuid>/image/<pk>/
    def delete(self, request, uuid, pk=None):
        try:
            image_obj = FarmInfoImage.objects.get(pk=pk, land_info__uuid=uuid)
        except FarmInfoImage.DoesNotExist:
            return Response({"detail": "이미지를 찾을 수 없습니다."},
                            status=status.HTTP_404_NOT_FOUND)
        
        image_obj.delete()
        return Response({"message": "이미지 삭제 완료"}, status=status.HTTP_204_NO_CONTENT)

def daum_post_view(request):
    return render(request, 'daum_postcode.html')
