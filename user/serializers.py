from .models import CustomUser, Type
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# from common.models import Address
# from common.serializers import AddressSerializer

from user.models import CustomUser

# from user.views import isNicePassDone
# from user.views import isEmailValidate

# from user.views import isNicePassDone
# from user.views import isEmailValidate

# from drf_yasg.utils import swagger_auto_schema
from . import swagger_doc


# 토큰에 원하는 정보 담기
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["uuid"] = str(user.uuid)  # UUID 인스턴스를 그냥 사용 불가능 -> str로 변형
        token["name"] = user.name
        token["email"] = user.email
        token["type"] = user.type
        # ...

        return token


class BaseUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    name = serializers.CharField(read_only=True)
    birthdate = serializers.CharField(read_only=True)
    gender = serializers.CharField(read_only=True)
    nationalinfo = serializers.CharField(read_only=True)
    mobileno = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            "name",
            "birthdate",
            "gender",
            "nationalinfo",
            "mobileno",
            "email",
            "type",
            "road",
            "jibun",
            "detail",
            "is_active",
        )


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, style={"input_type": "password"}, min_length=8
    )
    # address = serializers.JSONField(required=True)
    # email = serializers.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = [
            # "name",
            # "birthdate",
            # "gender",
            # "nationalinfo",
            # "mobileno",
            # "email",
            "password",
            "type",
            "road",
            "jibun",
            "detail",
        ]
        extra_kwargs = {
            "type": {"required": False, "default": Type.CUSTOMER},
            "gender": {"required": True},
            "nationalinfo": {"required": True},
        }

    # 비밀번호 검증 (패스워드와 확인용 패스워드 일치 여부)
    def validate(self, data):
        return data

    # 이메일 중복 확인
    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already in use.")
        return value

    # 주소 데이터 검증
    # def validate_address(self, value):
    #     required_fields = ["roadaddress", "jibunAddress", "detailAddress"]
    #     for field in required_fields:
    #         if field not in value:
    #             raise serializers.ValidationError(f"{field} is required in address.")
    #     return value

    # 사용자 생성
    def create(self, validated_data):
        # address_data = validated_data.pop("address", None)
        password = validated_data.pop("password")
        # 주소 생성
        # address = Address.objects.create(**address_data)
        # 사용자 생성
        user = CustomUser.objects.create_user(
            # address=address,
            password=password,
            **validated_data
        )
        return user


class ProfileSerializer(BaseUserSerializer):
    name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    mobileno = serializers.CharField(required=False)
    birthdate = serializers.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = [
            "name",
            "birthdate",
            "mobileno",
            "email",
            "road",
            "jibun",
            "detail",
        ]

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.email = validated_data.get("email", instance.email)
        instance.mobileno = validated_data.get("mobileno", instance.mobileno)
        instance.save()
        return instance


class ManageUserListSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        exclude = ("password",)


class UserLoginSerializer(serializers.Serializer):
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    uuid = serializers.UUIDField(read_only=True, format="hex_verbose")
    name = serializers.CharField(max_length=50, read_only=True)
    type = serializers.IntegerField(read_only=True)
    mobileno = serializers.CharField(read_only=True)
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(write_only=True, max_length=128)
    is_active = serializers.BooleanField(read_only=True)

    def create(self, validated_date):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        email = data["email"]
        password = data["password"]

        # TODO: 비밀번호가 맞지 않아도 로그인이 된다.
        # 위의 값을 이용해서 유저정보를 찾음, 유저 객체를 반환받음, is_active == False면 None
        user = authenticate(email=email, password=password)
        # 인증 실패 시, 비밀번호를 체크하여 더 상세한 오류를 처리
        if user is None:
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                raise serializers.ValidationError("아이디 또는 비밀번호를 잘못 입력함")

            # 비밀번호가 틀렸을 경우에 대한 오류 처리
            if not user.check_password(password):
                raise serializers.ValidationError("아이디 또는 비밀번호를 잘못 입력함")

            # 사용자가 비활성 상태일 때 처리
            if not user.is_active:
                raise serializers.ValidationError("인증을 확인중입니다.")

        try:
            # refresh = RefreshToken.for_user(user)
            refresh = CustomTokenObtainPairSerializer.get_token(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            update_last_login(None, user)
            # view에 넘길 데이터들
            validation = {
                "access": access_token,
                "refresh": refresh_token,
                "uuid": user.uuid,
                "name": user.name,
                "email": user.email,
                "type": user.type,
                "mobileno": user.mobileno,
                "is_active": user.is_active,
            }

            return validation
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials(유저 존재x)")
