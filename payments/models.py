from django.db import models

# 주소모델 지우고 각자에 할당하기
# 토스결제정보 저장


class TossPayments(models.Model):

    tossOrderId = models.CharField(
        max_length=65, blank=False, unique=True, null=False
    )  # 임의 생성 orderId
    paymentKey = models.CharField(
        max_length=100, blank=False, unique=True, null=False
    )  # 결제 정보조회, 취소 등에 쓰일 키
    method = models.CharField(max_length=10, blank=False)
    status = models.CharField(max_length=20, blank=False)
    totalAmount = models.IntegerField(
        blank=True, null=True
    )  # 총 결제금액 ex)신청서 여러개, 예약금 여러개일 경우

    # TODO:결제 날짜 추가하기 및 마이그레이션
    # paymentCompletedDate = models.DateField(auto_now=True)

    def __str__(self):
        return self.name
