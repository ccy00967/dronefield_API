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

    def validate_pnu(self, value):

        if not value or value.strip() == "":
            raise serializers.ValidationError("pnu 값은 비어 있을 수 없습니다.")
        return value

    def validate(self, data):

        required_fields = [
            "pnu",
            "lndpclAr",
            "cd",
            "landNickName",
            "road",
            "jibun",
            "detail",
        ]

        for field in required_fields:
            if not data.get(field) or str(data.get(field)).strip() == "":
                raise serializers.ValidationError(
                    {field: f"{field} 값은 비어 있을 수 없습니다."}
                )

        if "lndpclAr" in data and not data["lndpclAr"].isdigit():
            raise serializers.ValidationError(
                {"lndpclAr": "lndpclAr는 숫자여야 합니다."}
            )

        return data

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


# TODO: 나중에 최적화용 일부 데이터만 보내기
# class FarmInfoBriefSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FarmInfo
#         fields = ["landNickName", "cropsInfo"]
