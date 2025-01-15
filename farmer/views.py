from rest_framework import generics

from farmer.models import FarmInfo
from farmer.serializers import FarmInfoSerializer
from rest_framework.exceptions import NotFound
from rest_framework import permissions
from farmer.permissions import OnlyOwnerCanUpdate
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from common.utils.pageanation import CustomPagination
from rest_framework.permissions import IsAuthenticated
from django.db.models.deletion import ProtectedError
# from common.models import Address


# 농지목록 조회
class FarmInfoListView(generics.ListAPIView):
    queryset = FarmInfo.objects.all()
    serializer_class = FarmInfoSerializer
    name = "land_info_list"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,]
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
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
        serializer = FarmInfoSerializer(land_info, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # 신청서에 등록된 농지는 삭제 요청 불가능 하게 만들기
    def delete(self, request, uuid):
        try:
            land_info = self.get_object(uuid)
            land_info.delete()
            return Response(status=status.HTTP_204_NO_CONTENT, data={"message": "농지 정보가 삭제되었습니다."})
        except NotFound:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data={"message": "해당 농지 정보가 없거나 결제 중일 수 있습니다."}
            )

        except ProtectedError:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "삭제할 수 없는 농지입니다. 관련 데이터가 존재합니다."}
            )

        except Exception as e:
            # 알 수 없는 예외 처리
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={"message": f"알 수 없는 에러 발생: {str(e)}"}
            )
class TotalLandAreaAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 현재 사용자의 모든 땅 가져오기
        user_lands = FarmInfo.objects.filter(owner=request.user)
        total_area = user_lands.aggregate(total_lndpcAr=Sum('lndpcAr'))['total_lndpcAr'] or 0

        # 응답 데이터 직렬화 및 반환
        serializer = FarmInfoSerializer({'total_lndpcAr': total_area})
        return Response(serializer.data)
