from rest_framework import serializers
from farmrequest.models import CustomerRequest
from user.models import CustomUser


# 신청서에 방제사 정보 업데이트
class ExterminatorAcceptSerializer(serializers.ModelSerializer):
    orderid = serializers.ReadOnlyField()
    exterminatorinfo = CustomUser()

    class Meta:
        model=CustomerRequest
        fields= (
            'orderid',
            'exterminateState',
            'exterminatorinfo',
        )


# 방제 상황 업데이트
class ExterminateStateUpdateSerializer(serializers.ModelSerializer):
    orderid = serializers.ReadOnlyField()

    class Meta:
        model=CustomerRequest
        fields= (
            'orderid',
            'exterminateState',
        )