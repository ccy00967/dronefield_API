from rest_framework import generics
from rest_framework import permissions
#from exterminator.serializers import ExterminatorAcceptSerializer
#from exterminator.serializers import ExterminateStateUpdateSerializer

#from exterminator.permissions import OnlyExterminatorCanReadUpdate
from exterminator.permissions import CheckExterminateState
from exterminator.permissions import OnlyOwnerExterminatorCanUpdate

from trade.models import CustomerRequest
from trade.serializers import CustomerRequestSerializer

from farmer.models import ArableLandInfo
from rest_framework.response import Response

from exterminator.models import Exterminator
from exterminator.models import ExterminatorLicense
from exterminator.serializers import ExterminatorSerializer
from exterminator.serializers import ExterminatorLicenseSerializer


# # 방제사 라이선스
# class ExterminatorLicenseView(generics.ListCreateAPIView):
#     queryset = ExterminatorLicense.objects.all()
#     serializer_class = ExterminatorLicenseSerializer
#     lookup_field = "license_number"


# 방제사 정보
class ExterminatorView(generics.ListCreateAPIView):
    queryset = Exterminator.objects.all()
    serializer_class = ExterminatorSerializer
    lookup_field = "uuid"
    name = "exterminator-info"

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        OnlyOwnerExterminatorCanUpdate,
    ]


class ExterminatorLicenseView(generics.RetrieveUpdateAPIView):
    queryset = Exterminator.objects.all()
    serializer_class = ExterminatorLicenseSerializer
    lookup_field = "uuid"
    name = "exterminator-license"

    def patch(self, request, *args, **kwargs):
        # 'uuid'를 사용하여 Exterminator 객체를 찾음
        uuid = kwargs.get("uuid")
        # user__uuid=uuid는 Exterminator의 user 속성(즉, CustomUser 객체)의 uuid 필드가 요청받은 uuid와 일치하는 Exterminator 객체를 조회
        exterminator = Exterminator.objects.get(user__uuid=uuid)

        # Exterminator 객체에서 연결된 license 객체를 가져옴
        license_instance = exterminator.license

        # request의 데이터를 사용하여 license를 업데이트
        serializer = self.get_serializer(
            license_instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(request.data)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        OnlyOwnerExterminatorCanUpdate,
    ]


# # 방제사 정보 업데이트 - 방제 선점
# class ExtermCustomerRequestRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
#     queryset = CustomerRequest.objects.all()
#     serializer_class = ExterminatorAcceptSerializer
#     # lookup_field = 'orderid'
#     name = "exterminator-accept-deal"
#     permission_classes = (
#         permissions.IsAuthenticatedOrReadOnly,
#         OnlyExterminatorCanReadUpdate,
#         CheckExterminateState,
#     )

#     def perform_create(self, serializer):
#         orderIdList = self.request.data.get("orderidlist")

#         for orderid in orderIdList:
#             CustomerRequest.objects.filter(orderid=orderid).update(
#                 exterminatorinfo=self.request.user, exterminateState=1
#             )
#         # return Response({"message" : "결제가 완료되었습니다."}, status = status.HTTP_201_CREATED)


# # 방제사 정보 업데이트 - 방제 취소
# class ExterminatorAcceptUpdateDeleteView(generics.RetrieveDestroyAPIView):
#     queryset = CustomerRequest.objects.all()
#     serializer_class = ExterminatorAcceptSerializer
#     # lookup_field = 'orderid'
#     name = "exterminator-accept-cancel"

#     def perform_destroy(self, instance):
#         # serializer.save(exterminatorinfo=self.request.user)
#         serializer = self.get_serializer(instance, data=self.request.data)
#         serializer.save(exterminatorinfo=None, exterminateState=0)
#         # instance.delete()

#     permission_classes = (
#         permissions.IsAuthenticatedOrReadOnly,
#         OnlyExterminatorCanReadUpdate,
#         CheckExterminateState,
#     )


# # 방제 신청서 전부 가져오기
# class ExterminatorGetRequestsListView(generics.ListAPIView):
#     queryset = CustomerRequest.objects.all()
#     serializer_class = CustomerRequestSerializer
#     name = "exterminator-get-lists"
#     permission_classes = (
#         permissions.IsAuthenticatedOrReadOnly,
#         OnlyExterminatorCanReadUpdate,
#     )


# # 방제 신청서 cd로 전부 가져오기 - 위에 전부 가져오기랑 합칠수 있을듯
# class ExterminatorGetRequestsWithCdListView(generics.ListAPIView):
#     queryset = CustomerRequest.objects.all()
#     serializer_class = CustomerRequestSerializer
#     lookup_field = "cd"
#     name = "exterminator-get-cd-lists"
#     permission_classes = (
#         permissions.IsAuthenticatedOrReadOnly,
#         OnlyExterminatorCanReadUpdate,
#     )

#     def get_queryset(self):
#         return CustomerRequest.objects.filter(
#             landInfo__cd__startswith=str(self.kwargs["cd"])
#         )


# # 본인이 담당한 신청서만 가져오기 - 0,1,2,3 상태 넣기 - lookup field에
# class ExterminatorGetOwnRequestsListView(generics.ListAPIView):
#     queryset = CustomerRequest.objects.all()
#     serializer_class = CustomerRequestSerializer
#     lookup_field = "state"
#     name = "exterminator-get-own-lists"
#     permission_classes = (
#         permissions.IsAuthenticatedOrReadOnly,
#         OnlyExterminatorCanReadUpdate,
#     )

#     def get_queryset(self):
#         if self.kwargs["state"] == 1:  # 작업준비중
#             return CustomerRequest.objects.filter(
#                 exterminatorinfo=self.request.user, exterminateState=1
#             )
#         if self.kwargs["state"] == 2:  # 작업중
#             return CustomerRequest.objects.filter(
#                 exterminatorinfo=self.request.user, exterminateState=2
#             )
#         if self.kwargs["state"] == 3:  # 작업완료
#             return CustomerRequest.objects.filter(
#                 exterminatorinfo=self.request.user, exterminateState=3
#             )
#         return CustomerRequest.objects.filter(exterminatorinfo=self.request.user)


# # 방제 상태 변환하기
# class ExterminateStateUpdate(generics.RetrieveUpdateAPIView):
#     queryset = CustomerRequest.objects.all()
#     serializer_class = ExterminateStateUpdateSerializer
#     lookup_field = "orderid"
#     name = "exterminate-state-update"
#     permission_classes = (
#         permissions.IsAuthenticatedOrReadOnly,
#         OnlyOwnerExterminatorCanUpdate,
#         OnlyExterminatorCanReadUpdate,
#     )
