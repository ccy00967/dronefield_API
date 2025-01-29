from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import CustomUser
from django.utils import timezone
import uuid
import os

# Drone Exterminator License
class ExterminatorLicense(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    license_title = models.CharField(max_length=30, blank=True, null=True)
    license_number = models.CharField(max_length=30, blank=True, null=True)
    #lincense_nickname = models.CharField(max_length=30, blank=True, null=True)
    #model_number = models.CharField(max_length=30, blank=True, null=True)
    business_registration_type = models.CharField(max_length=30, blank=True, null=True)
    worker_registration_number = models.CharField(max_length=30, blank=True, null=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='exterminator_license')
    
    license_image = models.URLField(max_length=500, blank=True, null=True)
    business_registration_image = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.license_number} - {self.model_number}"

    class Meta:
        verbose_name = _("Exterminator License")
        verbose_name_plural = _("Exterminator Licenses")

# def drone_image_upload_to(instance, filename):
#     ext = filename.split('.')[-1]  # 파일 확장자
#     filename = f"{uuid.uuid4()}.{ext}"  # 고유한 파일 이름 생성
#     return os.path.join('drones/images', filename)  # 업로드 경로 반환

class Drone(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    nickname = models.CharField(max_length=30, blank=True, null=True)
    model_number = models.CharField(max_length=30, blank=True, null=True)
    capacity = models.CharField(max_length=30,blank=True, null=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='drones')
    image = models.URLField(max_length=500, blank=True, null=True)
    

    def __str__(self):
        return self.nickname if self.nickname else str(self.uuid)

    class Meta:
        verbose_name = _("Drone")
        verbose_name_plural = _("Drones")

