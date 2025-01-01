from .models import CustomUser
from exterminator.models import Exterminator
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from common.models import Address
from common.serializers import AddressSerializer

from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework_simplejwt.views import TokenObtainPairView

from user.models import CustomUser
from exterminator.models import Exterminator

from user.permissions import OnlyOwnerCanUpdate
from user.permissions import OnlyManagerCanAccess

#from user.views import isNicePassDone
#from user.views import isEmailValidate

from drf_yasg.utils import swagger_auto_schema
from . import swagger_doc

# 토큰에 원하는 정보 담기
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['uuid'] = str(user.uuid) # UUID 인스턴스를 그냥 사용 불가능 -> str로 변형
        token["name"] = user.name
        token["email"] = user.email
        token["role"] = user.role
        # ...

        return token


# 유저 가입을 담당하는 코드 - DB에 회원가입한 유저를 저장한다
class UserRegistrationSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    #role = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(read_only=True)
    password = serializers.CharField(write_only=True, max_length=128)
    # 나이스에서 세션으로 저장
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
            #"mobileco",
            #"nickname",
            "email",
            "password",
            "role",
            "address",
            "is_active",
        )
        # extra_kwargs = {
        #     "password" : {"write_only" : True},
        # }

    def create(self, validated_data):
        # 주소모델 인스턴스를 먼저 생성
        address = validated_data.pop('address')
        addressinfo = Address.objects.create(**address)
        auth_user = CustomUser.objects.create_user(address=addressinfo, **validated_data)
        return auth_user


# 유저의 로그인을 담당하는 코드 - 위의 커스텀토큰시리얼라이저와 연계
class UserLoginSerializer(serializers.Serializer):
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    uuid = serializers.UUIDField(read_only=True, format='hex_verbose')
    name = serializers.CharField(max_length=50, read_only=True)
    nickname = serializers.CharField(max_length=50, read_only=True)
    #role = serializers.CharField(read_only=True)
    role = serializers.IntegerField(read_only=True)
    mobileno = serializers.CharField(read_only=True)
    # address = AddressSerializer(read_only=True)
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

        # 위의 값을 이용해서 유저정보를 찾음, 유저 객체를 반환받음, is_active == False면 None
        user = authenticate(email=email, password=password)
        if user is None:
            user = CustomUser.objects.get(email=email)
            if user == None:
                raise serializers.ValidationError("아이디 또는 비밀번호를 잘못 입력함")
            
            is_active = getattr(user, 'is_active', None)
            if is_active == False:
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
                "uuid" : user.uuid,
                "name" : user.name,
                #"nickname": user.nickname,
                "email": user.email,
                "role": user.role,
                "mobileno" : user.mobileno,
                "is_active" : user.is_active,
            }

            return validation
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials(유저 존재x)")


class UserListSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    email = serializers.EmailField(read_only=True, max_length=100)
    role = serializers.IntegerField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            "name",
            "birthdate",
            "gender",
            "nationalinfo",
            #"mobileco",
            "mobileno",
            "email",
            "role",
            #"nickname",
            "address",
        )


class ManageUserListSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    #password = serializers.CharField(write_only=True, max_length=128)

    class Meta:
        model = CustomUser
        #fields = '__all__'
        exclude = ('password',)


# 방제사 회원가입 - 일반계정으로 가입시킨 후 매니저계정으로 업데이트
class ExterminatorSerializer(serializers.ModelSerializer):
    user = ManageUserListSerializer()
 
    class Meta:
        model = Exterminator
        fields = (
            'user',
            'license',
            'model_no', 
            'wrkr_no',
        )

