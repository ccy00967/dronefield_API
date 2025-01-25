from rest_framework import serializers
from farmer.models import FarmInfo, FarmInfoImage
from rest_framework import permissions
from .services.vworld import serch_pnu


# 농지 정보 등록
class FarmInfoSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.uuid")

    class Meta:
        model = FarmInfo
        fields = "__all__"

    def validate(self, data):
        if "lndpclAr" in data and not data["lndpclAr"].isdigit():
            raise serializers.ValidationError({"lndpclAr": "lndpclAr는 숫자여야 합니다."})
        
        return data
    
    def create(self, validated_data):
        try:
            serch_pnu_result = serch_pnu(jibun=validated_data["jibun"], road=validated_data["road"])
            validated_data["pnu"] = serch_pnu_result["pnu"]
            validated_data["cd"] = serch_pnu_result["adm_cd"]
            validated_data["lndpclAr"] = serch_pnu_result["lndpclAr"]
            instance = FarmInfo.objects.create(**validated_data)
            return instance
        except Exception as e:
            raise serializers.ValidationError({"message": f"에러 발생: {e}"})
    
    def update(self, instance, validated_data):
        try:
            if validated_data.get("road") or validated_data.get("jibun"):
                serch_pnu_result = serch_pnu(jibun=validated_data["jibun"], road=validated_data["road"])
                
                validated_data["pnu"] = serch_pnu_result["pnu"]
                validated_data["cd"] = serch_pnu_result["adm_cd"]
                validated_data["lndpclAr"] = serch_pnu_result["lndpclAr"]
                
            instance.landNickName = validated_data.get("landNickName", instance.landNickName)
            instance.cropsInfo = validated_data.get("cropsInfo", instance.cropsInfo)
            instance.additionalPhoneNum = validated_data.get("additionalPhoneNum", instance.additionalPhoneNum)
            instance.road = validated_data.get("road", instance.road)
            instance.jibun = validated_data.get("jibun", instance.jibun)
            instance.detail = validated_data.get("detail", instance.detail)
            instance.pnu = validated_data.get("pnu", instance.pnu)
            instance.lndpclAr = validated_data.get("lndpclAr", instance.lndpclAr)
            instance.cd = validated_data.get("cd", instance.cd)
            instance.save()
            return instance
        except Exception as e:
            raise serializers.ValidationError({"message": f"에러 발생: {e}"})


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
        fields = ['uuid', 'image', 'farm_info']

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
            FarmInfoImage.objects.create(farm_info=instance, image=image_file)
        return instance

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', [])
        instance.landNickName = validated_data.get('landNickName', instance.landNickName)
        instance.save()

        # ★ 여기서 'post=instance' 라고 되어 있는데, 실제 모델은 'farm_info'
        # => 아래처럼 수정
        for image_file in images_data:
            FarmInfoImage.objects.create(farm_info=instance, image=image_file)

        return instance
    
class FarmInfoImageDetailSerializer(serializers.ModelSerializer):
    images = FarmInfoImageSerializer(many=True, read_only=True, source='land_image')

    class Meta:
        model = FarmInfo
        fields = ['uuid', 'landNickName', 'images']