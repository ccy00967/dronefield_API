from rest_framework import serializers
from user.models import CustomUser
from exterminator.models import ExterminatorLicense, Drone
from django.urls import reverse

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
    image = serializers.ImageField(write_only=True, required=False)
    owner = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=CustomUser.objects.all(),
        required=False
    )

    class Meta:
        model = Drone
        fields = "__all__"

    
    
    def get_image(self, obj):
        if obj.image:
            request = self.context.get('request')
            return request.build_absolute_uri(
                reverse('drone-image', args=[obj.pk])
            )
        return None

    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)