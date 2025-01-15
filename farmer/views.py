from rest_framework import generics
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from farmer.permissions import OnlyOwnerCanUpdate

from django.db.models.functions import Cast
from django.db.models import FloatField
from farmer.models import FarmInfo
from farmer.serializers import FarmInfoSerializer
from farmer.serializers import FarmInfoUpdateSerializer
from farmer.serializers import FarmInfoBriefSerializer
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from common.utils.pageanation import CustomPagination
from trade.models import Request


# 농지목록 조회
class FarmInfoListView(generics.ListAPIView):
    queryset = FarmInfo.objects.all()
    serializer_class = FarmInfoBriefSerializer
    name = "land_info_list"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset().filter(owner=self.request.user)
        if self.request.query_params.get("owner"):
            owner = self.request.query_params.get("owner")
            queryset = queryset.filter(owner__uuid=owner)
        return queryset


class FarmInfoCreateView(generics.CreateAPIView):
    queryset = FarmInfo.objects.all()
    serializer_class = FarmInfoSerializer
    name = "land_info_create"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # 신청한 유저 정보를 함께 저장
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


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
        land_info = self.get_object(uuid)
        serializer = FarmInfoSerializer(land_info)
        return Response(serializer.data)

    def patch(self, request, uuid):
        land_info = self.get_object(uuid)
        serializer = FarmInfoUpdateSerializer(land_info, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # 신청서에 등록된 농지는 삭제 불가능
    def delete(self, request, uuid):
        try:
            land_info = self.get_object(uuid)
            if Request.objects.filter(farm_info=land_info).exists():
                return Response(
                    status=status.HTTP_400_BAD_REQUEST,
                    data={"message": "이 농지 정보는 다른 요청에 참조 중이어서 삭제할 수 없습니다."}
                )
            land_info.delete()
            return Response(status=status.HTTP_204_NO_CONTENT, data={"message": "농지 정보가 삭제되었습니다."})
        # except NotFound:
        #     return Response(status=status.HTTP_404_NOT_FOUND, data={"message": "해당 농지 정보가 없습니, 결재중일 수 있습니다."})
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
