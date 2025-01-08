from django.db import models
import uuid


# 농지 정보
class ArableLandInfo(models.Model):
    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False, db_index=True
    )
    owner = models.ForeignKey(
        "user.CustomUser", related_name="land_owner", on_delete=models.CASCADE
    )

    # 네이버 MAPS API, 주소정보
    road = models.CharField(max_length=50, blank=True, default="")
    jibun = models.CharField(max_length=50, blank=False, default="")
    detail = models.CharField(max_length=50, blank=False, default="")

    # 디지털트윈 토지임야정보 API
    pnu = models.CharField(
        max_length=30, blank=False, null=False, default=""
    )  # 농지 고유번호
    lndpclAr = models.CharField(
        max_length=50, blank=False, null=False, default=""
    )  # 면적 m^2

    cd = models.CharField(max_length=8, blank=False, null=False, default="")  # 행정구역

    # 농지 추가 정보
    landNickName = models.CharField(max_length=50, blank=False, default="")  # 농지 별칭
    cropsInfo = models.CharField(max_length=50, blank=False, default="")  # 농작물 정보
    additionalPhoneNum = models.CharField(max_length=50, blank=True, default="")

    def __str__(self):
        return self.landNickName
