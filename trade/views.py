import math
from rest_framework import generics
from rest_framework import permissions

from trade.models import CustomerRequest
from trade.serializers import CustomerRequestSerializer
from trade.serializers import CustomerRequestBriefSerializer
from trade.serializers import CustomerCheckExterminateStateSerializer

from farmer.models import ArableLandInfo

from trade.permissions import OnlyOwnerCanUpdate
from trade.permissions import isBeforePay


# 신청서 등록
# 토스 페이먼츠 적용대상 - 신청서 모델 생성후 토스 정보를 받아서 토스 모델 생성연결
class CustomerRequestCreateAPIView(generics.CreateAPIView):
    queryset = CustomerRequest.objects.all()
    serializer_class = CustomerRequestSerializer
    # landInfo의 uuid
    lookup_field = "landuuid"
    #name = "customer-request-list"
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def perform_create(self, serializer):
        landinfo = ArableLandInfo.objects.get(uuid=self.kwargs.get('landuuid'))
        setAveragePrice = self.request.data['setAveragePrice']
        serializer.save(
            owner=self.request.user, 
            landInfo=landinfo,
            requestAmount= math.ceil(float(setAveragePrice) * float(landinfo.lndpclAr) * 0.3025),
        )

    # def get_queryset(self):
    #     user = self.request.user
    #     return CustomerRequest.objects.filter(owner=user)    

# 신청서 목록
# 토스 페이먼츠 적용대상 - 신청서 모델 생성후 토스 정보를 받아서 토스 모델 생성연결
class CustomerRequestListAPIView(generics.ListAPIView):
    queryset = CustomerRequest.objects.all()
    serializer_class = CustomerRequestSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        #OnlyOwnerCanUpdate,
    )  

    def get_queryset(self):
        return CustomerRequest.objects.filter(owner=self.request.user)


# 신청서 수정
# 결제완료 후에는 수정 못하게 막기 - permission추가하기
class CustomerRequestListUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomerRequest.objects.all()
    serializer_class = CustomerRequestSerializer
    # CustomerRequest의 uuid == orderid
    lookup_field = "orderid"
    name = "customer-request_update"
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        OnlyOwnerCanUpdate,
        isBeforePay,
    )


# 방제 신청

# 방제 상태 수정 - 농민, 드론방제업자 STATE 두개 만들기

# 정산 - 신안은행 대금이체 API 사용 예정?
# class RequestExterminateDoneView(generics.RetrieveUpdateDestroyAPIView):
# 금액 정산 시리얼라이저 필요?
# 신청서 수정
# 결제완료 후에는 수정 못하게 막기 - permission추가하기

# 농민 방제 확인 상태
class CustomerCheckExterminateStateRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    queryset = CustomerRequest.objects.all()
    serializer_class = CustomerCheckExterminateStateSerializer
    # CustomerRequest의 uuid == orderid
    lookup_field = "orderid"
    name = "customer-request_update"
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        OnlyOwnerCanUpdate,
    )