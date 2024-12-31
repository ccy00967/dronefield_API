from rest_framework import serializers;
from common.models import Address;
from common.models import TossPayments;
from farmrequest.models import CustomerRequest;


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model=Address
        fields = '__all__'


class TossPaymentsSerializer(serializers.ModelSerializer):
    cancelReason = serializers.CharField(max_length=100, )

    class Meta:
        model=TossPayments
        fields = '__all__'


# 신청서와 예약금 2개 만들기
class TossPaymentsUpdateSerializer(serializers.ModelSerializer):
    orderid = serializers.ReadOnlyField()
    #tosspayments = TossPayments.objects.get(orderId='orderId')

    class Meta:
        model=CustomerRequest
        fields= (
            'orderid',
            'requestTosspayments',
        )
