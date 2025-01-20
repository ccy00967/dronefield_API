from rest_framework import serializers
from farmer.models import FarmInfo, FarmInfoImage


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

class FarmInfoImageSerializer(serializers.ModelSerializer): 
    class Meta:
        model = FarmInfoImage
        fields = ['uuid', 'image', 'land_info']

class FarmInfoImageCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        write_only=True,
        required=False
    )
    class Meta:
        model = FarmInfo
        fields = ['uuid', 'images', 'landNickName']
    
    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        # FarmInfo 생성 (owner는 context 등에서 가져오거나 perform_create에서 주입)
        instance = FarmInfo.objects.create(
            owner=self.context['request'].user,
            **validated_data
        )
        # 여러 이미지 생성
        for image_file in images_data:
            FarmInfoImage.objects.create(land_info=instance, image=image_file)
        return instance

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        instance.landNickName = validated_data.get('landNickName', instance.landNickName)
        instance.save()

        # ★ 여기서 'post=instance' 라고 되어 있는데, 실제 모델은 'farm_info'
        # => 아래처럼 수정
        for image_file in images_data:
            FarmInfoImage.objects.create(land_info=instance, image=image_file)

        return instance
    
class FarmInfoImageDetailSerializer(serializers.ModelSerializer):
    images = FarmInfoImageSerializer(many=True, read_only=True, source='land_image')

    class Meta:
        model = FarmInfo
        fields = ['uuid', 'landNickName', 'images']