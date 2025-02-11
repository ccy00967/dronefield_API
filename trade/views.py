import math
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import api_view
from common.utils.filters import RequestFilter
from trade.models import Request
from trade.serializers import RequestSerializer
from trade.serializers import RequestDetailSerializer
from trade.serializers import RequestBriefSerializer
from trade.serializers import RequestUpdateSerializer
from trade.serializers import CheckStateSerializer
from trade.serializers import ExterminateStateSerializer
from user.models import CustomUser

from farmer.models import FarmInfo

from trade.permissions import OnlyOwnerCanUpdate
from trade.permissions import OnlyOnChargeExterminator
from trade.permissions import isBeforePay

from common.utils.pageanation import CustomPagination


# 면적(평)당 방제가격 계산기
def servicePriceCal(setAveragePrice, lndpclAr):
    setAveragePrice = float(setAveragePrice)
    lndpclAr = float(lndpclAr)
    servicePrice = setAveragePrice * lndpclAr * 0.3025
    return servicePrice


# 방제 상태별 개수 - 계정 주인 것만 보이기
@api_view(("GET",))
def count_by_exterminateState(request):
    type = request.user.type

    queryset = None

    if type == 3:
        queryset = Request.objects.filter(exterminator=request.user)
    if type == 4:
        queryset = Request.objects.filter(owner=request.user)
    # Check if queryset is None
    if queryset is None:
        return Response({"detail": "Invalid User provided!"}, status=400)

    try:
        before_pay_count = queryset.filter(exterminateState=0, requestDepositState=0).count()
        matching_count = queryset.filter(exterminateState=0, requestDepositState=1).count()
        preparing_count = queryset.filter(exterminateState=1, requestDepositState=1).count()
        exterminating_count = queryset.filter(exterminateState=2, requestDepositState=1).count()
        done_count = queryset.filter(exterminateState=3, requestDepositState=1).count()
    except Exception as e:
        return Response({"message": f"Error occurred while counting: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    return Response(
        {
            "before_pay_count": before_pay_count,
            "matching_count": matching_count,
            "preparing_count": preparing_count,
            "exterminating_count": exterminating_count, #방제결제 이후 아이템 수수
            "done_count": done_count,
        },
        status=200,
    )


# 신청서 등록
# 토스 페이먼츠 적용대상 - 신청서 모델 생성후 토스 정보를 받아서 토스 모델 생성연결
class RequestCreateAPIView(generics.CreateAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    # landInfo의 uuid
    lookup_field = "landuuid"
    name = "request-list"
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # TODO: REFACTOR: 시리얼라이저로 옮기기
    def perform_create(self, serializer):
        landinfo = FarmInfo.objects.get(uuid=self.kwargs.get("landuuid"))
        setAveragePrice = self.request.data["setAveragePrice"]#평단가
        price = (int(servicePriceCal(setAveragePrice, landinfo.lndpclAr))//10)*10
        serializer.save(
            owner=self.request.user,
            landInfo=landinfo,
            requestAmount=math.ceil(price),
        )
        


# 신청서 목록 - 농민용
class FarmerRequestListAPIView(generics.ListAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestBriefSerializer
    pagination_class = CustomPagination
    name = "request-lists"
    ordering_fields = [
        "landNickName",
        "cropsInfo",
        "landInfo__lndpclAr",
    ]
    ordering = [
        "landInfo__landNickName",
    ]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = RequestFilter
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        # OnlyOwnerCanUpdate,
    )

    def get_queryset(self):
        queryset = Request.objects.filter(owner=self.request.user)

        # 클라이언트에서 값을 쿼리 파라미터로 받아서 필터링 - exterminateState가 RequestFilter로 이동됨
        # exterminate_state = self.request.query_params.get("exterminateState", None)
        requestDeposit_state = self.request.query_params.get(
            "requestDepositState", None
        )
        
        # if exterminate_state is not None:
        #     try:
        #         exterminate_state = int(exterminate_state)
        #         if exterminate_state in [0, 1, 2, 3]:
        #             queryset = queryset.filter(exterminateState=exterminate_state)
        #     except ValueError:
        #         pass  # exterminateState 값이 유효하지 않으면 필터링하지 않음

        if requestDeposit_state is not None:
            try:
                requestDeposit_state = int(requestDeposit_state)
                if requestDeposit_state in [0, 1, 2]:
                    queryset = queryset.filter(requestDepositState=requestDeposit_state)
            except ValueError:
                pass  # exterminateState 값이 유효하지 않으면 필터링하지 않음

        # exterminateState가 없는 경우엔 모든 데이터를 반환
        return queryset


# 신청서 목록 - 방제사용
class ExterminatorRequestListAPIView(generics.ListAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestBriefSerializer
    pagination_class = CustomPagination
    name = "exterminator-request-lists"
    pagination_class = CustomPagination
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        # OnlyOwnerCanUpdate,
    )

    def get_queryset(self):
        # TODO: 결제된 신청서만 보이게 필터링하는 코드
        #queryset = Request.objects.filter(exterminateState=0, exterminator=None, checkState=0, requestDepositState=1)
        queryset = Request.objects.filter(exterminateState=0, exterminator=None, checkState=0,)
        cd = self.request.query_params.get("cd", None)

        if cd is not None:
            try:
                queryset = queryset.filter(landInfo__cd__startswith=str(cd))
            except ValueError:
                pass  # cd 값이 유효하지 않으면 필터링하지 않음

        return queryset


# 담당중인 방제목록 가져오기 - 방제사용
class ExterminatorWorkRequestListAPIView(generics.ListAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestBriefSerializer
    pagination_class = CustomPagination
    name = "exterminator-work-request-lists"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] 
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = RequestFilter
    ordering_fields = ['startDate', 'endDate', 'orderId', 'exterminateState']
    ordering = ['startDate']
    
    def get_queryset(self):
        # user = CustomUser.objects.get(email=self.request.user)
        # print(user)
        # queryset = Request.objects.filter(exterminator__email=user)
        queryset = Request.objects.filter(exterminator__email=self.request.user)
        # if queryset == test_queryset:
        #     print("queryset is same")
        # else:
        #     print(queryset)
        #     print(test_queryset)
        return queryset 
    

# 담당중인 신청서 상세 가져오기 - 방제사용
class ExterminatorWorkRequestRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestBriefSerializer
    lookup_field = "orderId"
    name = "exterminator-work-request-detail"
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )


# 신청서 수정 - 결제 전에만 가능
class RequestUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestUpdateSerializer
    # Request의 uuid == orderid
    lookup_field = "orderId"
    name = "request-detail-update"
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        OnlyOwnerCanUpdate,
        #isBeforePay,
    )
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "신청서가 성공적으로 삭제되었습니다."},
            status=status.HTTP_200_OK
        )


# 농민이 방제사가 잘 했나 확인
class CheckStateUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Request.objects.all()
    serializer_class = CheckStateSerializer
    lookup_field = "orderId"
    name = "farmer-check-exterminate"
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        OnlyOwnerCanUpdate,
    )
    #체크포인트 1이면
    #체크포인트 2이면면
    def patch(self, request, *args, **kwargs):
        # PATCH 요청의 데이터에서 checkState 값을 가져오기
        check_state = request.data.get("checkState")
    
        # checkState가 None이거나 빈 문자열인 경우 처리
        if check_state is None or check_state == "":
            return Response(
                {"error": "checkState is required."},
                status=400
            )
    
        # checkState를 정수로 변환 시도
        try:
            check_state = int(check_state)  # 문자열을 정수로 변환
        except ValueError:
            return Response(
                {"error": "Invalid value for checkState. It must be an integer."},
                status=400
            )
    
        # checkState가 유효한 값(1, 2, 3)인지 확인
        if check_state not in [1, 2, 3]:
            return Response(
                {"error": "Invalid value for checkState. It must be one of [1, 2, 3]."},
                status=400
            )
    
        # 유효하면 기존의 partial_update 호출
        return self.partial_update(request, *args, **kwargs)


# 방제 진행 상태 변경
class ExterminateStateUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Request.objects.all()
    serializer_class = ExterminateStateSerializer
    lookup_field = "orderId"
    name = "exterminator-exterminate"
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        #OnlyOnChargeExterminator, #TODO: 방제사만 가능하게 다시 수정
    )
    
    def patch(self, request, *args, **kwargs):
        # PATCH 요청의 데이터에서 exterminateState 값을 가져오기
        exterminate_state = request.data.get("exterminateState")
    
        # exterminateState가 None이거나 빈 문자열인 경우 처리
        if exterminate_state is None or exterminate_state == "":
            return Response(
                {"error": "exterminateState is required."},
                status=400
            )
    
        # exterminateState를 정수로 변환 시도
        try:
            exterminate_state = int(exterminate_state)  # 문자열을 정수로 변환
        except ValueError:
            return Response(
                {"error": "Invalid value for exterminateState. It must be an integer."},
                status=400
            )
    
        # exterminateState가 유효한 값(1, 2, 3)인지 확인
        #if exterminate_state not in [1, 2, 3]:
        if exterminate_state not in [0, 1, 2, 3]: # 테스트용으로 0도 허용  
            return Response(
                {"error": "Invalid value for exterminateState. It must be one of [1, 2, 3]."},
                status=400
            )
        
        #현재 인스턴스 가져오기
        instance = self.get_object()

        # exterminator 필드를 현재 로그인한 사용자로 설정
        instance.exterminator = request.user

        # 인스턴스 상태를 데이터베이스에 저장
        instance.save()
        
        # 유효하면 기존의 partial_update 호출
        return self.partial_update(request, *args, **kwargs)
