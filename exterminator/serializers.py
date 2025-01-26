from rest_framework import serializers
from user.models import CustomUser
from exterminator.models import ExterminatorLicense

class ExterminatorLicenseSerializer(serializers.ModelSerializer):
    license_number = serializers.CharField(max_length=30, required=True)
    model_number = serializers.CharField(max_length=30, required=True)
    worker_registration_number = serializers.CharField(max_length=30, required=True)
    owner = serializers.ReadOnlyField(source="owner.uuid")

    class Meta:
        model = ExterminatorLicense
        fields ="__all__"

    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)