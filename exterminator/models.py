from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import CustomUser
from django.utils import timezone
import uuid


# Drone Exterminator License
class ExterminatorLicense(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    license_number = models.CharField(max_length=30, blank=True, null=True)
    lincense_nickname = models.CharField(max_length=30, blank=True, null=True)
    #model_number = models.CharField(max_length=30, blank=True, null=True)
    worker_registration_number = models.CharField(max_length=30, blank=True, null=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='exterminator_license')
    
    license_image = models.ImageField(
        upload_to='licenses/license_images/',
        verbose_name=_("License Image"),
        null=True,  # 이미지가 필수가 아닐 경우 True로 설정
        blank=True
    )
    
    # 사업자등록증 이미지 필드 추가
    business_registration_image = models.ImageField(
        upload_to='licenses/business_registration_images/',
        verbose_name=_("Business Registration Image"),
        null=True,  # 이미지가 필수가 아닐 경우 True로 설정
        blank=True
    )

    def __str__(self):
        return f"{self.license_number} - {self.model_number}"

    class Meta:
        verbose_name = _("Exterminator License")
        verbose_name_plural = _("Exterminator Licenses")

class Drone(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    nickname = models.CharField(max_length=30, blank=True, null=True)
    model_number = models.CharField(max_length=30, blank=True, null=True)
    capacity = models.FloatField(blank=True, null=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='drones')
    image = models.ImageField(
        upload_to='drones/images/',
        verbose_name=_("Drone Image"),
        null=True,  # 이미지가 필수가 아닐 경우 True로 설정
        blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Drone")
        verbose_name_plural = _("Drones")

