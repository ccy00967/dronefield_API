from rest_framework import serializers
from trade.models import Request
from user.serializers import ProfileSerializer
from payments.serializers import TossPaymentsSerializer
from farmer.serializers import FarmInfoSerializer


# 신청서
class RequestSerializer(serializers.ModelSerializer):
    orderId = serializers.ReadOnlyField()
    owner = ProfileSerializer(read_only=True)
    exterminator = ProfileSerializer(read_only=True)
    landInfo = FarmInfoSerializer(read_only=True)
    # 유저가 수정하면 안되는 것들
    calculation = serializers.ReadOnlyField()
    requestAmount = serializers.ReadOnlyField()
    requestDepositState = serializers.ReadOnlyField()
    reservateDepositState = serializers.ReadOnlyField()

    class Meta:
        model = Request
        # fields='__all__'
        exclude = (
            "requestCancelTransactionKey",
            "depositCancelTransactionKey",
            # "requestTosspayments",
            # "reservateTosspayments",
        )


# 신청서 세부정보 - 오직 GET인 View에서만 사용하기
class RequestDetailSerializer(serializers.ModelSerializer):
    landInfo = FarmInfoSerializer(read_only=True)
    requestTosspayments = TossPaymentsSerializer(read_only=True)
    reservateTosspayments = TossPaymentsSerializer(read_only=True)

    class Meta:
        model = Request
        fields='__all__'
        # exclude = (
        # )


# 신청서 업데이트
class RequestUpdateSerializer(serializers.ModelSerializer):
    owner = serializers.UUIDField(source="owner.uuid")
    exterminator = serializers.UUIDField(source="exterminator.uuid", required=False, allow_null=True)
    landInfo = FarmInfoSerializer(read_only=True)
    requestTosspayments = TossPaymentsSerializer(read_only=True)
    reservateTosspayments = TossPaymentsSerializer(read_only=True)

    class Meta:
        model = Request
        # fields=(
        #     "endDate",
        #     "pesticide",
        # )
        fields="__all__"
        read_only_fields = (
            "orderId",
            "owner",
            "exterminator",
            "landInfo",
            "exterminateState",
            "checkState",
            "calculation",
            "dealmothod",
            "startDate",
            "extraDetails",
            # "endDate",
            # "pesticide",
            "setAveragePrice",
            "requestAmount",
            "requestDepositState",
            "requestCancelTransactionKey",
            "reservateDepositAmount",
            "reservateDepositState",
            "depositCancelTransactionKey",
            "requestTosspayments",
            "reservateTosspayments"
        )


# 읽기(GET) 전용에만 사용
class RequestBriefSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source="landInfo.owner.name")
    owner_mobileno = serializers.CharField(source="landInfo.owner.mobileno")
    exterminator = ProfileSerializer(read_only=True)
    landNickName = serializers.CharField(source="landInfo.landNickName")
    cropsInfo = serializers.CharField(source="landInfo.cropsInfo")
    jibun = serializers.CharField(source="landInfo.jibun")
    lndpclAr = serializers.CharField(source="landInfo.lndpclAr")
    cd = serializers.CharField(source="landInfo.cd")

    class Meta:
        model = Request
        fields = (
            "owner_name",
            "owner_mobileno",
            "orderId",
            "cd",
            "exterminator",
            "landNickName",
            "cropsInfo",
            "jibun",
            "lndpclAr",
            "startDate",
            "endDate",
            "pesticide",
            "extraDetails",
            "exterminateState",
            "requestDepositState",
            # "reservateDepositState",
            "checkState",
            "calculation",
            "requestAmount",
            "requestTosspayments",
            "reservateTosspayments",
        )


# 결제완료 후 신청서에 방제상태 업데이트
# 농민용 방제 완료 확인
class CheckStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = (
            "checkState",
        )


# 방제사용 방제 상태 관리
class ExterminateStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = (
            "exterminateState",
        )