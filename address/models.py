from django.db import models


# 집주소, 농지 주소 저장
class Address(models.Model):

    # + 집주소인지, 농지주소인지 구분할 type 필요
    roadaddress = models.CharField(max_length=50, blank=True, default="")
    jibunAddress = models.CharField(max_length=50, blank=False, default="")
    detailAddress = models.CharField(max_length=50, blank=False, default="")

    def __str__(self):
        return self.name
