import math
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view

from trade.models import Request
from trade.serializers import RequestBriefSerializer
from trade.serializers import RequestSerializer
from trade.serializers import CheckExterminateStateSerializer

from farmer.models import FarmInfo

from trade.permissions import OnlyOwnerCanUpdate
from trade.permissions import isBeforePay

from common.utils.pageanation import CustomPagination


# 면적(평)당 방제가격 계산기
def servicePriceCal(setAveragePrice, lndpclAr):
    setAveragePrice = float(setAveragePrice)
    lndpclAr = float(lndpclAr)
    servicePrice = setAveragePrice * lndpclAr * 0.3025
    return servicePrice


    # before_pay_count = Request.objects.filter(requestDepositState=0).count()
    # matching_count = (
    #     Request.objects.filter(exterminateState=0).count() - before_pay_count
    # )
    # preparing_count = Request.objects.filter(exterminateState=1).count()
    # exterminating_count = Request.objects.filter(exterminateState=2).count()
    # done_count = Request.objects.filter(exterminateState=3).count()


# 방제 상태별 개수 - 계정주인 것만 보이기
@api_view(("GET",))
def count_by_exterminateState(request):
    type = request.query_params.get("type", None)

    print("---------")
    print(type)
    # Initialize queryset
    queryset = None

    if type is not None:
        if type == "3" :
            queryset = Request.objects.filter(exterminator=request.user)
        if type == "4" :
            queryset = Request.objects.filter(owner=request.user)

    # Check if queryset is None
    if queryset is None:
        return Response({"detail": "Invalid type or no type provided."}, status=400)

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
        queryset = Request.objects.filter(requestDepositState=1, exterminateState=0)
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
        # OnlyOwnerCanUpdate,
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


# 신청서 수정 - 결제완료 후에는 수정 못하게 막기
class RequestListUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    # CustomerRequest의 uuid == orderid
    lookup_field = "orderId"
    name = "request-detail-update"
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        OnlyOwnerCanUpdate,
        isBeforePay,
    )


# 농민 방제 확인 상태
class CheckExterminateStateRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = Request.objects.all()
    serializer_class = CheckExterminateStateSerializer
    # CustomerRequest의 uuid == orderid
    lookup_field = "orderid"
    name = "request_state_update"
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        OnlyOwnerCanUpdate,
    )


# 방제 신청

# 방제 상태 수정 - 농민, 드론방제업자 STATE 두개 만들기

# 정산 - 신안은행 대금이체 API 사용 예정?
# class RequestExterminateDoneView(generics.RetrieveUpdateDestroyAPIView):
# 금액 정산 시리얼라이저 필요?
# 신청서 수정
# 결제완료 후에는 수정 못하게 막기 - permission추가하기

