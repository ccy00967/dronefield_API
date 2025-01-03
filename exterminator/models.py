from django.db import models
from django.utils.translation import gettext_lazy as _
from user.models import CustomUser


# Drone Exterminator License
class ExterminatorLicense(models.Model):
    license_number = models.CharField(max_length=30, blank=False)
    model_number = models.CharField(max_length=30, blank=False)
    worker_registration_number = models.CharField(max_length=30, blank=False)

    def __str__(self):
        return f"{self.license_number} - {self.model_number}"

    class Meta:
        verbose_name = _("Exterminator License")
        verbose_name_plural = _("Exterminator Licenses")


# Exterminator Model
class Exterminator(models.Model):
    user = models.OneToOneField(
        CustomUser,
        related_name="exterminator_profile",  # Unique related_name to avoid clashes
        on_delete=models.PROTECT,
    )
    license = models.OneToOneField(
        ExterminatorLicense,
        related_name="license_for_exterminator",  # More descriptive to avoid conflicts
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.user.name} - {self.license.license_number}"

    class Meta:
        verbose_name = _("Exterminator")
        verbose_name_plural = _("Exterminators")
