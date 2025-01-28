from rest_framework import serializers
from user.models import CustomUser
from exterminator.models import ExterminatorLicense, Drone
from django.urls import reverse
import uuid
from django.core.files.storage import default_storage
from common.utils.s3 import s3_upload_file

class ExterminatorLicenseSerializer(serializers.ModelSerializer):
    license_image = serializers.ImageField(write_only=True, required=False)
    business_registration_image = serializers.ImageField(write_only=True, required=False)
    owner = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=CustomUser.objects.all(),
        required=False
    )

    class Meta:
        model = ExterminatorLicense
        fields ="__all__"
        
    def validate(self, attrs):
        #user = self.context['request'].user
        #if ExterminatorLicense.objects.filter(owner=user).exists():
        #    raise serializers.ValidationError("이미 라이선스가 등록되어 있습니다.")
        return attrs
    
    def get_license_image(self, obj):
        if obj.license_image:
            request = self.context.get('request')
            return request.build_absolute_uri(
                reverse('exterminator-license-image', args=[obj.pk, 'license_image'])
            )
        return None

    def get_business_registration_image(self, obj):
        if obj.business_registration_image:
            request = self.context.get('request')
            return request.build_absolute_uri(
                reverse('exterminator-license-image', args=[obj.pk, 'business_registration_image'])
            )
        return None
    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class ExterminatorLicenseImageSerializer(serializers.ModelSerializer):
    license_image = serializers.ImageField(required=True)
    business_registration_image = serializers.ImageField(required=True)

    class Meta:
        model = ExterminatorLicense
        fields = ["license_image", "business_registration_image"]

    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class DroneSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(write_only=True, required=False)  # POST 요청에서 이미지를 파일로 받음
    image_url = serializers.URLField(read_only=True, source='image')  # 응답에서 S3 URL 반환
    owner = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=CustomUser.objects.all(),
        required=False
    )

    class Meta:
        model = Drone
        fields = ['uuid', 'nickname', 'model_number', 'capacity', 'owner', 'image', 'image_url']
    
    def create(self, validated_data):
        image_file = validated_data.pop('image', None)
        if image_file:
            # S3에 저장될 파일 이름 생성
            file_name = f'drones/images/{uuid.uuid4()}.jpg'

            # S3에 파일 업로드
            s3_url = s3_upload_file(image_file, file_name)  # 파일 객체를 직접 S3로 업로드
            if not s3_url:
                raise serializers.ValidationError({"image": "S3에 파일 업로드에 실패했습니다."})

            # 업로드된 S3 URL 저장
            validated_data['image'] = s3_url

        return super().create(validated_data)
        
    def update(self, instance, validated_data):
        image_file = validated_data.pop('image', None)
        if image_file:
            # S3에 저장될 파일 이름 생성
            file_name = f'drones/images/{uuid.uuid4()}.jpg'
    
            # S3에 파일 업로드
            s3_url = s3_upload_file(image_file, file_name)
            if not s3_url:
                raise serializers.ValidationError({"image": "S3에 파일 업로드에 실패했습니다."})
    
            # 업로드된 S3 URL을 validated_data에 추가
            validated_data['image'] = s3_url
    
        # 기존 인스턴스를 업데이트
        return super().update(instance, validated_data)