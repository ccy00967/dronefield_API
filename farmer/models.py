from django.db import models
import uuid

# 농지 정보


class FarmInfo(models.Model):
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

    pnu = models.CharField(
        max_length=30, blank=False, null=False, default=""
    )  # 디지털트윈 토지임야정보 API
    lndpclAr = models.CharField(max_length=50, blank=True, null=True)  # 농지 고유번호
    # 면적 m^2
    cd = models.CharField(max_length=10, blank=False, null=False, default="")  # 행정구역

    # 농지 추가 정보
    landNickName = models.CharField(max_length=50, blank=False, default="")  # 농지 별칭
    cropsInfo = models.CharField(max_length=50, blank=False, default="")  # 농작물 정보
    additionalPhoneNum = models.CharField(max_length=50, blank=True, default="") # 추가 연락처
    min_price = models.PositiveIntegerField(blank=False, null=False, default=0)# 최소 가격
    
    #point_x = models.FloatField(default=0)
    #point_y = models.FloatField(default=0)
    
    def __str__(self):
        return self.landNickName


#TODO: 나중에 이미지처리
class FarmInfoImage(models.Model):
    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False, db_index=True
    )
    farm_info = models.ForeignKey(
        FarmInfo, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="farm_info/images/")
    created_at = models.DateTimeField(auto_now_add=True)