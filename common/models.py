# from django.db import models
# from django.utils.translation import gettext_lazy as _


# class Type(models.TextChoices):
#     HOME = "H", _("Home")
#     FARM = "F", _("FARM")


# class Address(models.Model):

#     type = models.CharField(max_length=1, choices=Type.choices, blank=False)
#     road = models.CharField(max_length=50, blank=True, default="")
#     jibun = models.CharField(max_length=50, blank=False, default="")
#     detail = models.CharField(max_length=50, blank=False, default="")

#     def __str__(self):
#         return self.name
