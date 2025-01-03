from django.db import models
import uuid


# 농지 정보
class ArableLandInfo(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, db_index=True)
    owner = models.ForeignKey('user.CustomUser',related_name = 'land_owner',on_delete=models.CASCADE)

    # 디지털트윈 토지임야정보 API
    pnu = models.CharField(max_length=30, blank=False, null=False, default='')
    lndpclAr = models.CharField(max_length=50, blank=False, null=False, default='')

    # 네이버 MAPS API
    address = models.ForeignKey('common.Address',related_name = 'land_address',on_delete=models.CASCADE)

    # 행정구역
    cd = models.CharField(max_length=8, blank=False, null=False, default='')

    #농지 추가 정보
    landNickName = models.CharField(max_length=50, blank=False, default='')
    cropsInfo = models.CharField(max_length=50, blank=False, default='')
    additionalPhoneNum = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.landNickName
