from rest_framework import serializers
from trade.models import Request
from user.serializers import ProfileSerializer
from payments.serializers import TossPaymentsSerializer
from farmer.serializers import FarmInfoSerializer


# 신청서
class RequestSerializer(serializers.ModelSerializer):
    # 외래키인 owner.[내용물]로 값을 리턴받을 수 있다, 물론 아래 Meta클래스의 필드에도 추가해야한다
    # tosspaymentorderId = serializers.ReadOnlyField(source='owner.uuid')
    # requestownerName = serializers.ReadOnlyField(source="requestowner.name")
    # requestownerEmail = serializers.ReadOnlyField(source="requestowner.email")
    orderId = serializers.ReadOnlyField()
    owner = ProfileSerializer(read_only=True)
    exterminator = ProfileSerializer(read_only=True)
    landInfo = FarmInfoSerializer(read_only=True)
    # 유저가 수정하면 안되는 것들
    calculation = serializers.ReadOnlyField()
    requestAmount = serializers.ReadOnlyField()
    requestDepositState = serializers.ReadOnlyField()
    reservateDepositState = serializers.ReadOnlyField()

    # 유저가 수정하는 목록
    """
    exterminateState 오직 방제사용
    customerCheckState
    dealmothod
    startDate
    pesticide
    setAmount
    """

    class Meta:
        model = Request
        # fields='__all__'
        exclude = (
            "requestCancelTransactionKey",
            "depositCancelTransactionKey",
            # "requestTosspayments",
            # "reservateTosspayments",
        )


# 금액 정산 시리얼라이저 필요?
class RequestExterminateDoneSerializer(serializers.ModelSerializer):
    orderid = serializers.ReadOnlyField()

    class Meta:
        model = Request
        fields = (
            "orderId",
            "calculation",
        )


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
            "exterminateState",
            "requestDepositState",
            # "reservateDepositState",
            "checkState",
            "calculation",
        )


class CheckExterminateStateSerializer(serializers.ModelSerializer):
    orderid = serializers.ReadOnlyField()

    class Meta:
        model = Request
        fields = (
            "orderid",
            "customerCheckState",
        )
