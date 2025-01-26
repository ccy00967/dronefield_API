from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import CustomUser
from django.utils import timezone
import uuid


# Drone Exterminator License
class ExterminatorLicense(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    license_number = models.CharField(max_length=30, blank=False, null=False)
    model_number = models.CharField(max_length=30, blank=False, null=False)
    worker_registration_number = models.CharField(max_length=30, blank=False, null=False)
    owner = models.ForeignKey("user.CustomUser", related_name="exterminator_license", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.license_number} - {self.model_number}"

    class Meta:
        verbose_name = _("Exterminator License")
        verbose_name_plural = _("Exterminator Licenses")

