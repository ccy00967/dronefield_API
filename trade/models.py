from django.db import models
import uuid


DEAL_METHOD_CHOICES = (
    (0, "normal"),
    (1, "personal"),
)

EXTERMINATE_STATE = (
    (0, "matching"),  # 매칭중
    (1, "preparing"),  # 작업준비중
    (2, "exterminating"),  # 작업중
    (3, "done"),  # 작업완료
)

CHECK_STATE = (
    (0, "checking"),
    (1, "done"),
)

CALCULATION = (
    (0, "checking"),
    (1, "success"),
    (2, "cancel"),
)


# 방제 신청서
class Request(models.Model):
    # id와 uuid따로 존재
    orderId = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    # 신청유저정보
    owner = models.ForeignKey(
        "user.CustomUser",
        related_name="request_owner",
        on_delete=models.PROTECT,
    )
    # 담당 방제사 정보
    exterminator = models.ForeignKey(
        "user.CustomUser",
        related_name="request_exterminator",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
    )
    # 농지정보
    landInfo = models.ForeignKey(
        "farmer.FarmInfo",
        related_name="request_landInfo",
        on_delete=models.PROTECT,
    )
    # 거래 방식
    dealmothod = models.PositiveSmallIntegerField(
        choices=DEAL_METHOD_CHOICES,
        blank=False,
        default=0,
    )
    # 날짜
    startDate = models.DateField()
    endDate = models.DateField()
    # 농약종류
    pesticide = models.CharField(max_length=50, blank=True, default="")
    # 평단가 - 일반거래 30원 고정
    setAveragePrice = models.IntegerField(blank=False, null=False, default=0)
    # 신청서 가격
    requestAmount = models.PositiveIntegerField(blank=False, null=False, default=0)
    # 방제사 예약 금액
    reservateDepositAmount = models.PositiveIntegerField(
        blank=False, null=False, default=1000
    )
    # 신청서 토스 결제정보 - 총 가격을 토스 모델이 가짐ex) 신청서 여러개
    requestTosspayments = models.ForeignKey(
        "payments.TossPayments",
        related_name="request_tosspayments",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    # 예약금 토스 결제정보 - 총 가격을 토스 모델이 가짐 ex) 예약금 여러개
    reservateTosspayments = models.ForeignKey(
        "payments.TossPayments",
        related_name="reservate_tosspayments",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )

    # 농민용
    # 방제완료 확인 - 농민용
    checkState = models.PositiveSmallIntegerField(
        choices=CHECK_STATE, blank=False, default=0
    )
    # 신청서 결제 상태
    requestDepositState = models.PositiveSmallIntegerField(
        choices=CALCULATION, blank=False, default=0
    )
    # 신청서 결제 취소 토스 키
    requestCancelTransactionKey = models.CharField(
        max_length=80, blank=True, default=""
    )

    # 방제사용
    # 방제진행 상황 - 방제사용
    exterminateState = models.PositiveSmallIntegerField(
        choices=EXTERMINATE_STATE, blank=False, default=0
    )
    # 방제 예약금
    reservateDepositState = models.PositiveSmallIntegerField(
        choices=CALCULATION, blank=False, default=0
    )
    # 예약금 결제 취소 토스 키
    depositCancelTransactionKey = models.CharField(
        max_length=80, blank=True, default=""
    )
   

    # 드론평야용 - 정산상황 - 대금 정산완료 시 여기값을 1로 변경
    calculation = models.PositiveSmallIntegerField(
        choices=CALCULATION, blank=False, default=0
    )

    def __str__(self):
        return str(self.orderId)
    
class BankAccount(models.Model):
    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False, db_index=True
    )
    owner = models.ForeignKey(
        "user.CustomUser",
        related_name="bank_owner",
        on_delete=models.PROTECT,
    )
    bankName = models.CharField(max_length=50, blank=False, default="")
    accountNumber = models.CharField(max_length=50, blank=False, default="")
    accountType = models.CharField(max_length=50, blank=False, default="")
    accountCreated = models.DateTimeField(auto_now_add=True)
    accountUpdated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.bankName
