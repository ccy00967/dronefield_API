from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework_simplejwt.views import TokenObtainPairView

from ..auth.models import CustomUser
from ..auth.models import Exterminator

from ..auth.serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer, 
    UserListSerializer,
    CustomTokenObtainPairSerializer,
    ManageUserListSerializer,
    ExterminatorSerializer,
)

from auth.permissions import OnlyOwnerCanUpdate
from auth.permissions import OnlyManagerCanAccess

from auth.views import isNicePassDone
from auth.views import isEmailValidate

from drf_yasg.utils import swagger_auto_schema
from . import swagger_doc


# 토큰2개(refresh, access)를 발급한다
# 안쓸것 같으니까 나중에 주석처리하기
# class CustomTokenObtainPairView(TokenObtainPairView):
#     serializer_class = CustomTokenObtainPairSerializer


# 유저 회원가입 - 이메일, 비밀번호 사용
class UserRegistrationView(generics.GenericAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_id='회원가입',
        operation_description='유저 회원가입',
        tags=['user'],
        responses=swagger_doc.UserRegistrationResponse,
    )
    def post(self, request):
        # 나중에 permission으로 이동하기
        # NicePass 본인인증 여부 확인
        if(request.session.get(isNicePassDone) != True):
            print("나이스 본인인증이 안됨!")
            return Response({"message": "nicepass validation need first"}, status=status.HTTP_401_UNAUTHORIZED)
        # 이메일 인증 여부 확인
        if(request.session.get(isEmailValidate) != True):
            print("이메일 인증이 안됨!")
            return Response({"message": "email validation need first"}, status=status.HTTP_401_UNAUTHORIZED)
        # 방제사라면 인증후 직접 바꾸어줌
        if(request.data["role"] == 3):
            print("방제사는 나중에 서류 확인 후 activate 시켜줌")
            is_active = False
        else : 
            is_active = True

        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            # 데이터베이스에 유저정보 저장(serializer create실행)
            serializer.save(
                name = request.session.get("name"),
                birthdate = request.session.get("birthdate"),
                gender = request.session.get("gender"),
                nationalinfo = request.session.get("nationalinfo"),
                mobileno = request.session.get("mobileno"),
                email = request.session.get("email"),
                is_active=is_active,
            )
            request.session.flush() #세션의 모든 것을 삭제
            request.session.save()

            response = {
                "success": True,
                "message": "User successfully registered!",
            }
            return Response(response, status=status.HTTP_201_CREATED)


# 이메일과 비밀번호로 로그인
class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        operation_id='로그인',
        operation_description='유저 로그인',
        tags=['user'],
        responses=swagger_doc.UserLoginResponse,
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK
            # 유저로그인시리얼라이저의 validation 참고해서 작성
            response = {
                "access": serializer.data["access"],
                "refresh": serializer.data["refresh"],
                "uuid" : serializer.data["uuid"],
            }

            return Response(response, status=status_code)
        return Response({"message": "Login Not Success"}, status=status.HTTP_401_UNAUTHORIZED)


# 사용자 정보를 수정 - 오직 자기자신의 정보만 수정가능 - access토큰으로 인증
class UserDataUpdateView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserListSerializer
    lookup_field = "uuid"

    permission_classes = [
        IsAuthenticated,
        OnlyOwnerCanUpdate,
    ]


class ExterminatorView(generics.ListAPIView):
    queryset = Exterminator.objects.all()
    serializer_class = ExterminatorSerializer
    lookup_field = "uuid"

    permission_classes = [
        IsAuthenticated,
        OnlyOwnerCanUpdate,
    ]

'''
# 관리자용 유저정보 수정
# 농민에서 방제사로 변경등에 필요
class ManageUserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ManageUserListSerializer

    permission_classes = [
        IsAuthenticated,
        OnlyManagerCanAccess,
    ]


class ManageUserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ManageUserListSerializer
    lookup_field = "uuid"
    permission_classes = [
        IsAuthenticated,
        OnlyManagerCanAccess,
    ]

# 방제사 정보 업데이트 - 관리자계정으로 일반계정을 방제사로 업데이트
class ManageExterminatorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ExterminatorSerializer
    lookup_field = "uuid"
    permission_classes = [
        IsAuthenticated,
        OnlyManagerCanAccess,
    ]

    def perform_create(self, serializer):
        #!중요 - 바로 시리얼라이저의 모델 requestowner에게 전달된다
        serializer.save(user=CustomUser.objects.get(uuid=self.lookup_field))
'''

    # 중요!
    # 토큰을 입력받으면 자동으로 디코딩되어 request에 담기는 것 같다
    # 결론) 뷰에는 queryset으로 데이터를 가져오고
    # 보여질 데이터는 시리얼라이저에서 제한하기
    # 퍼미션스파일에 여러가지 퍼미션을 만들어서 유져용, 어드민용을 만들기!
    # 즉, 뷰파일을 깔끔하게 유지하고 로직들을 전부 퍼미션 파일로 옮긴다
