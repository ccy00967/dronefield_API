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
    uuid = models.UUIDField(db_index=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=16, blank=False, editable=False)
    birthdate = models.CharField(max_length=8, blank=False, editable=False)
    gender = models.CharField(max_length=1, choices=Gender.choices, blank=False, editable=False)
    nationalinfo = models.CharField(max_length=1, choices=Nation.choices, blank=False, editable=False)
    mobileno = models.CharField(max_length=14, unique=True, blank=False)
    email = models.EmailField(max_length=30, unique=True, blank=False)
    type = models.PositiveSmallIntegerField(choices=Type.choices, default=Type.CUSTOMER)
    road = models.CharField(max_length=50, blank=True, default="")
    jibun = models.CharField(max_length=50, blank=False, default="")
    detail = models.CharField(max_length=50, blank=False, default="")
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    optinal_consent = models.BooleanField(default=False)
    marketing_agreement_date = models.DateTimeField(null=True, blank=True)
    required_consent_data = models.DateTimeField(null=True, blank=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        
class BankAccount(models.Model):
    uuid = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False, db_index=True
    )
    owner = models.ForeignKey(
        "user.CustomUser",
        related_name="bank_owner",
        on_delete=models.PROTECT,
    )
    bank_name = models.CharField(max_length=50, blank=False, default="")
    account_number = models.CharField(max_length=50, blank=False, default="")
    account_type = models.CharField(max_length=50, blank=False, default="")
    account_created = models.DateTimeField(auto_now_add=True)
    account_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.bank_name