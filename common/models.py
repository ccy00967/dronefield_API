from django.db import models

class Address(models.Model):

    roadaddress = models.CharField(max_length=50, blank=True, default="")
    jibunAddress = models.CharField(max_length=50, blank=False, default="")
    detailAddress = models.CharField(max_length=50, blank=False, default="")


    def __str__(self):
        return self.name