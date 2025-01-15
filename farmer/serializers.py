from rest_framework import serializers
from farmer.models import FarmInfo


# 농지 정보 등록
class FarmInfoSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.uuid")

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


# 농지 정보 수정
class FarmInfoUpdateSerializer(serializers.ModelSerializer):
    uuid = serializers.ReadOnlyField()
    owner = serializers.ReadOnlyField(source="owner.uuid")
    road = serializers.ReadOnlyField()
    jibun = serializers.ReadOnlyField()
    pnu = serializers.ReadOnlyField()
    lndpclAr = serializers.ReadOnlyField()
    cd = serializers.ReadOnlyField()

    class Meta:
        model = FarmInfo
        fields = "__all__"


# TODO: 나중에 최적화용 일부 데이터만 보내기
class FarmInfoBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmInfo
        fields = [
            "uuid",
            "landNickName",
            "lndpclAr",
            "jibun",
            "road",
            "cropsInfo",
        ]
