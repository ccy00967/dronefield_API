from rest_framework import serializers
from user.models import CustomUser
from exterminator.models import Exterminator
from exterminator.models import ExterminatorLicense


class ExterminatorLicenseSerializer(serializers.ModelSerializer):
    license_number = serializers.CharField(max_length=30, required=True)
    model_number = serializers.CharField(max_length=30, required=True)
    worker_registration_number = serializers.CharField(max_length=30, required=True)

    class Meta:
        model = ExterminatorLicense
        fields = (
            "license_number",
            "model_number",
            "worker_registration_number",
        )


class ExterminatorSerializer(serializers.ModelSerializer):
    user = CustomUser()
    license = ExterminatorLicense()

    class Meta:
        model = Exterminator
        fields = (
            "user",
            "license",
        )

    def validate_user(self, value):
        if CustomUser.objects.filter(uuid=value).exists():
            raise serializers.ValidationError("CustomUser Info Create Needed")
        return value

    def validate_license(self, value):
        if ExterminatorLicense.objects.filter(license_number=value).exists():
            raise serializers.ValidationError("Extermintor License Info Create Needed")
        return value

    def create(self, validated_date):
        uuid = validated_date.pop("uuid")
        license_number = validated_date.pop("license_number")

        user = CustomUser.objects.filter(uuid=uuid)
        license = ExterminatorLicense.objects.filter(license_number=license_number)

        exterminator = Exterminator.objects.create(user=user, license=license)
        return exterminator

    # # 라이선스 부분적 업데이트 - 유저 정보 수정은 user에서 관리?
    # # 특이하다 생각하는점 - ExterminatorLicenseSerializer를 update하는데 ExterminatorSerializer가 가지고 있다는 점이다.
    # def update(self, instance, validated_data):
    #     license_data = validated_data.get("license", None)

    #     # license 업데이트
    #     if license_data:
    #         # license 객체의 필드를 업데이트하는 방식
    #         license_instance = instance.license
    #         for field, value in license_data.items():
    #             # 만약 license 모델에 해당 필드가 존재하면 업데이트, 단 속성 네이밍이 같아야함
    #             if hasattr(license_instance, field):
    #                 setattr(license_instance, field, value)

    #         # 업데이트된 license 저장
    #         license_instance.save()

    #     # 변경된 instance 저장
    #     instance.save()
