import uuid
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
import re
from django.utils.translation import gettext_lazy as _


class Type(models.IntegerChoices):
    ADMIN = 1, _("Admin")
    MANAGER = 2, _("Manager")
    DRONE_EXTERMINATOR = 3, _("Drone Exterminator")
    CUSTOMER = 4, _("Customer")


class Gender(models.TextChoices):
    FEMALE = "0", _("Woman")
    MALE = "1", _("Man")


class Nation(models.TextChoices):
    LOCAL = "0", _("Domestic")
    FOREIGN = "1", _("Foreigner")


class CustomUserManager(BaseUserManager):

    def _validate_password(self, password):
        if len(password) < 8:
            raise ValueError(_("Password must be at least 8 characters long."))
        if not re.search(r"[a-zA-Z]", password):
            raise ValueError(_("Password must contain at least one letter."))
        if not re.search(r"\d", password):
            raise ValueError(_("Password must contain at least one number."))
        if not re.search(r"[!@#$%^&*()]", password):
            raise ValueError(
                _("Password must contain at least one special character (!@#$%^&*()).")
            )

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_("Email is required."))
        self._validate_password(password)

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_manager(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("type", Type.MANAGER)
        return self.create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("type", Type.ADMIN)

        if extra_fields.get("type") != Type.ADMIN:
            raise ValueError(_("Superuser must have type of Admin"))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(
        db_index=True, unique=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(max_length=16, blank=False)
    birthdate = models.CharField(max_length=8, blank=False)
    gender = models.CharField(max_length=1, choices=Gender.choices, blank=False)
    nationalinfo = models.CharField(max_length=1, choices=Nation.choices, blank=False)
    mobileno = models.CharField(max_length=14, unique=True, blank=False)
    email = models.EmailField(max_length=30, unique=True, blank=False)
    type = models.PositiveSmallIntegerField(choices=Type.choices, default=Type.CUSTOMER)
    # address = models.ForeignKey(
    #     "common.Address",
    #     related_name="useraddress",
    #     on_delete=models.CASCADE,
    #     blank=True,
    #     null=True,
    # )
    road = models.CharField(max_length=50, blank=True, default="")
    jibun = models.CharField(max_length=50, blank=False, default="")
    detail = models.CharField(max_length=50, blank=False, default="")
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
