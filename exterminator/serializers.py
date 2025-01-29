from rest_framework import serializers
from user.models import CustomUser
from exterminator.models import ExterminatorLicense, Drone
from django.urls import reverse
import uuid
from django.core.files.storage import default_storage
from common.utils.s3 import s3_upload_file, s3_delete_file

class ExterminatorLicenseSerializer(serializers.ModelSerializer):
    license_image = serializers.ImageField(write_only=True, required=False)  # POST 요청에서 이미지를 파일로 받음
    license_image_url = serializers.URLField(read_only=True, source='license_image')  # 응답에서 S3 URL 반환
    business_registration_image = serializers.ImageField(write_only=True, required=False)  # POST 요청에서 이미지를 파일로 받음
    business_registration_image_url = serializers.URLField(read_only=True, source='business_registration_image')  # 응답에서 S3 URL 반환
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
    
    def create(self, validated_data):
        license_image_file = validated_data.pop('license_image', None)
        business_registration_image_file = validated_data.pop('business_registration_image', None)
        uuid_key= uuid.uuid4()
        
        if license_image_file:
            file_name = f'exterminator/images/license/{uuid_key}.jpg'
    
            s3_url = s3_upload_file(license_image_file, file_name)
            if not s3_url:
                raise serializers.ValidationError({"license_image": "S3에 파일 업로드에 실패했습니다."})

            validated_data['license_image'] = s3_url
        
        if business_registration_image_file:
            file_name = f'exterminator/images/business/{uuid_key}.jpg'
    
            s3_url = s3_upload_file(business_registration_image_file, file_name)
            if not s3_url:
                raise serializers.ValidationError({"business_registration_image": "S3에 파일 업로드에 실패했습니다."})

            validated_data['business_registration_image'] = s3_url
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        license_image_file = validated_data.pop('license_image', None)
        business_registration_image_file = validated_data.pop('business_registration_image', None)
        uuid_key = uuid.uuid4()

        # 기존 이미지 삭제 후 새 이미지 업로드
        if license_image_file:
            if instance.license_image:  # 기존 이미지가 있다면 삭제
                s3_delete_file(instance.license_image)

            license_image_name = f'exterminator/images/license/{uuid_key}.jpg'
            license_s3_url = s3_upload_file(license_image_file, license_image_name)
            validated_data['license_image'] = license_s3_url

        if business_registration_image_file:
            if instance.business_registration_image:  # 기존 이미지가 있다면 삭제
                s3_delete_file(instance.business_registration_image)

            business_registration_image_name = f'exterminator/images/business/{uuid_key}.jpg'
            business_registration_url = s3_upload_file(business_registration_image_file, business_registration_image_name)
            validated_data['business_registration_image'] = business_registration_url

        return super().update(instance, validated_data)

    
    def delete(self, instance):
        
        return super().delete(instance)


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
            file_name = f'drones/images/{uuid.uuid4()}.jpg'

            s3_url = s3_upload_file(image_file, file_name)
            if not s3_url:
                raise serializers.ValidationError({"image": "S3에 파일 업로드에 실패했습니다."})

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
    
            validated_data['image'] = s3_url
    
        # 기존 인스턴스를 업데이트
        return super().update(instance, validated_data)