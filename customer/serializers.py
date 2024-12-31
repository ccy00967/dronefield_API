from rest_framework import serializers
from customer.models import ArableLandInfo
from farmrequest.models import CustomerRequest
from common.models import Address
from common.serializers import AddressSerializer


# 농지 정보 등록
class ArableLandInfoSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.uuid')
    address = AddressSerializer()
    
    class Meta:
        model=ArableLandInfo
        fields='__all__'


    # 주소정보 모델 인스턴생 생성및 저장
    def create(self, validated_data):
        address = validated_data.pop('address')
        addressinfo = Address.objects.create(**address)
        arableland = ArableLandInfo.objects.create(
            address=addressinfo,
            **validated_data,
        )
        return arableland

