import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
import re


ADMIN = 1
MANAGER = 2
DRONE_EXTERMINATOR = 3
CUSTOMER = 4

# LOCAL = 0
# ALIEN = 1
# WOMAN = 0
# MAN = 1

ROLE_CHOICES = (
    (ADMIN, "Admin"),
    (MANAGER, "Manager"),
    (DRONE_EXTERMINATOR, "Drone_exterminator"),
    (CUSTOMER, "Customer"),
)
GENDERS = (
    ("0", "여성(Woman)"),
    ("1", "남성(Man)"),
)
NATION = (
    ("0", "내국인"),
    ("1", "외국인"),
)


# 헬퍼 클래스
class CustomUserManager(BaseUserManager):

    # 일반 유저
    def create_user(self, email, password, **extra_fields):

        # 주어진 이메일, 비밀번호 등 개인정보로 User 인스턴스 생성
        if not email:
            raise ValueError("Users must email valid first")
        if len(password) < 8:
            raise ValueError("비밀번호는 8자리 이상이어야 합니다.")
        if not re.search(r"[a-zA-Z]", password):
            raise ValueError("비밀번호는 하나 이상의 영문이 포함되어야 합니다.")
        if not re.search(r"\d", password):
            raise ValueError("비밀번호는 하나 이상의 숫자가 포함되어야 합니다.")
        if not re.search(r"[!@#$%^&*()]", password):
            raise ValueError(
                "비밀번호는 적어도 하나 이상의 특수문자(!@#$%^&*())가 포함되어야 합니다."
            )

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields,
        )

        user.set_password(password)

        user.save(using=self._db)
        return user

    # 드론평야 관리자
    def create_manager(self, email=None, password=None, **extra_fields):

        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", 2)

        if extra_fields.get("role") != 2:
            raise ValueError("Superuser must have role of Global Admin")

        return self.create_user(email, password, **extra_fields)


# 현재 데이터베이스에 유저정보가 정수형으로 순차적으로 입력된다 - user_id?이건가?
# 유니크키값으로 바꾸기 - 겹치지 않는 고유값으로 수정하기
# AbstractBaseUser를 상속해서 유저 커스텀
class CustomUser(AbstractBaseUser, PermissionsMixin):

    uuid = models.UUIDField(
        db_index=True, unique=True, default=uuid.uuid4, editable=False
    )

    # 나이스 pass에서 받은 정보
    name = models.CharField(max_length=16, blank=False, default="", unique=False)
    birthdate = models.CharField(max_length=8, blank=False, null=False)
    gender = models.CharField(max_length=1, choices=GENDERS, blank=False, null=False)
    nationalinfo = models.CharField(
        max_length=1, choices=NATION, blank=False, null=False
    )
    # mobileco = models.CharField(max_length=1, blank=False, null=False)
    mobileno = models.CharField(max_length=14, unique=True, blank=False, null=False)

    # 드론평야 추가 정보
    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES, blank=True, null=True, default=4
    )
    # nickname = models.CharField(max_length=15, blank=True, default="", unique=True)
    email = models.EmailField(max_length=30, unique=True, null=False, blank=False)

    address = models.ForeignKey(
        "common.Address",
        related_name="useraddress",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    # 유저 기본정보
    # 시리얼라이저에서 이메일을 인증하면 세션에서 is_active==True로 전달 후 저장
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 사용자의 username field는 email으로 설정 (이메일로 로그인)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # 헬퍼 클래스 사용
    objects = CustomUserManager()

    def __str__(self):
        return self.email


# 수정필요 - 농민, 방제사 각각의 APP에 위의 User정보를 외래키로 저장 [User] <- [농민], [방제사]
# 방제사 정보 추가하기
class Exterminator(models.Model):

    user = models.ForeignKey(
        CustomUser,
        related_name="exterminatorInfo",
        on_delete=models.PROTECT,
    )

    # 조종자격증
    license = models.CharField(max_length=30, blank=False, null=False)
    # 기체모델
    model_no = models.CharField(max_length=30, blank=False, null=False)
    # 사업자등록증번호
    wrkr_no = models.CharField(max_length=30, blank=False, null=False)
