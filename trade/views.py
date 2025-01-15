import math
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view

from trade.models import Request
from trade.serializers import RequestSerializer
from trade.serializers import RequestDetailSerializer
from trade.serializers import RequestBriefSerializer
from trade.serializers import RequestUpdateSerializer
from trade.serializers import CheckStateSerializer
from trade.serializers import ExterminateStateSerializer

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

    before_pay_count = queryset.filter(requestDepositState=0).count()
    matching_count = (
        queryset.filter(exterminateState=0).count() - before_pay_count
    )
    preparing_count = queryset.filter(exterminateState=1).count()
    exterminating_count = queryset.filter(exterminateState=2).count()
    done_count = queryset.filter(exterminateState=3).count()

    return Response(
        {
            "before_pay_count": before_pay_count,
            "matching_count": matching_count,
            "preparing_count": preparing_count,
            "exterminating_count": exterminating_count,
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

    def perform_create(self, serializer):
        landinfo = FarmInfo.objects.get(uuid=self.kwargs.get("landuuid"))
        setAveragePrice = self.request.data["setAveragePrice"]
        price = servicePriceCal(setAveragePrice, landinfo.lndpclAr)
        serializer.save(
            owner=self.request.user,
            landInfo=landinfo,
            requestAmount=math.ceil(price),
        )

    # def get_queryset(self):
    #     user = self.request.user
    #     return CustomerRequest.objects.filter(owner=user)


# 신청서 목록 - 농민용
class FarmerRequestListAPIView(generics.ListAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestBriefSerializer
    name = "request-lists"
    ordering_fields = [
        "landNickName",
        "cropsInfo",
        "landInfo__lndpclAr",
    ]
    ordering = [
        "landInfo__landNickName",
    ]
    pagination_class = CustomPagination
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        # OnlyOwnerCanUpdate,
    )

    def get_queryset(self):
        queryset = Request.objects.filter(owner=self.request.user)

        # 클라이언트에서 값을 쿼리 파라미터로 받아서 필터링
        exterminate_state = self.request.query_params.get("exterminateState", None)
        requestDeposit_state = self.request.query_params.get(
            "requestDepositState", None
        )

        if exterminate_state is not None:
            try:
                exterminate_state = int(exterminate_state)
                if exterminate_state in [0, 1, 2, 3]:
                    queryset = queryset.filter(exterminateState=exterminate_state)
            except ValueError:
                pass  # exterminateState 값이 유효하지 않으면 필터링하지 않음

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
    name = "exterminator-request-lists"
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        # OnlyOwnerCanUpdate,
    )

    def get_queryset(self):
        queryset = Request.objects.filter(requestDepositState=1, exterminateState=0, exterminator=None)
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
    name = "exterminator-work-request-lists"
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def get_queryset(self):
        queryset = Request.objects.filter(exterminator=self.request.user)
        exterminate_state = self.request.query_params.get("exterminateState", None)

        if exterminate_state is not None:
            try:
                exterminate_state = int(exterminate_state)
                if exterminate_state in [0, 1, 2, 3]:
                    queryset = queryset.filter(exterminateState=exterminate_state)
            except ValueError:
                pass  # exterminateState 값이 유효하지 않으면 필터링하지 않음

        return queryset
    

# 담당중인 신청서 상세 가져오기 - 방제사용
class ExterminatorWorkRequestRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestDetailSerializer
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
        isBeforePay,
    )


# 농민이 방제사가 잘 했나 확인인
class CheckStateUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Request.objects.all()
    serializer_class = CheckStateSerializer
    lookup_field = "orderId"
    name = "farmer-check-exterminate"
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        OnlyOwnerCanUpdate,
    )


# 방제 진행 상태 변경
class ExterminateStateUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Request.objects.all()
    serializer_class = ExterminateStateSerializer
    lookup_field = "orderId"
    name = "exterminator-exterminate"
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        OnlyOnChargeExterminator,
    )

    def patch(self, request, *args, **kwargs):
        # PATCH 요청의 데이터에서 exterminateState 값을 가져오기
        exterminate_state = request.data.get("exterminateState")

        # exterminateState가 유효한 값(1, 2, 3, 4)인지 확인
        if exterminate_state not in [1, 2, 3, 4]:
            return Response(
                {"error": "Invalid value for exterminateState. It must be one of [1, 2, 3, 4]."},
                status=400
            )

        # 유효하면 기존의 partial_update 호출
        return self.partial_update(request, *args, **kwargs)

#TODO: 환불 로직 만들기 - 결제된 신청서의 삭제는 환불로직을 따름