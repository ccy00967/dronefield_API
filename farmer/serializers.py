from rest_framework import serializers
from farmer.models import FarmInfo

# from common.models import Address
# from common.serializers import AddressSerializer


# 농지 정보 등록
class FarmInfoSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.uuid")
    # address = AddressSerializer()

    class Meta:
        model = FarmInfo
        fields = "__all__"

    # 주소정보 모델 인스턴생 생성및 저장
    # def create(self, validated_data):
    #     address = validated_data.pop("address")
    #     addressinfo = Address.objects.create(**address)
    #     arableland = FarmInfo.objects.create(
    #         address=addressinfo,
    #         **validated_data,
    #     )
    #     return arableland

    # def update(self, instance, validated_data):
    #     address = validated_data.pop("address")
    #     addressinfo = instance.address

    #     addressinfo.road = address.get("road", addressinfo.road)
    #     addressinfo.jibun = address.get("jibun", addressinfo.jibun)
    #     addressinfo.detail = address.get("detail", addressinfo.detail)

    #     addressinfo.save()

    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)

    #     instance.save()
    #     return instance
