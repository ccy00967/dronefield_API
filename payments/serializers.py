from rest_framework import serializers
from payments.models import TossPayments
from trade.models import Request


class TossPaymentsSerializer(serializers.ModelSerializer):
    cancelReason = serializers.CharField(
        max_length=100,
    )

    class Meta:
        model = TossPayments
        fields = "__all__"


# TODO: 신청서와 예약금 2개 만들기
class TossPaymentsUpdateSerializer(serializers.ModelSerializer):
    orderid = serializers.ReadOnlyField()
    # tosspayments = TossPayments.objects.get(orderId='orderId')

    class Meta:
        model = Request
        fields = (
            "orderid",
            "requestTosspayments",
        )
