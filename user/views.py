import base64, requests, time, random, json, hashlib, hmac
from datetime import datetime
import uuid
from rest_framework import status
from django.core.mail import EmailMessage
from django.core.cache import cache
from django.contrib.sessions.models import Session
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework_simplejwt.views import TokenBlacklistView
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.timezone import now

# from drf_yasg.utils import swagger_auto_schema
from . import swagger_doc
from rest_framework.permissions import AllowAny
from django.shortcuts import render
from .service.Nice.utils import encrypt_data
from .service.Nice.utils import decrypt_data
from .service.Nice.utils import clientID
from .service.Nice.utils import secretKey
from .service.Nice.utils import APIUrl
from .service.Nice.utils import productID
from .service.Nice.utils import access_token

# from .nice_fuc import returnURL
from user.models import CustomUser, BankAccount
from .permissions import OnlyOwnerCanUpdate
from rest_framework import generics
from exterminator.models import ExterminatorLicense
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from user.serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    ProfileSerializer,
    CustomTokenObtainPairSerializer,
    ManageUserListSerializer,
    BankAccountSerializer,
    UserChurnReasonSerializer
    # ExterminatorSerializer,
)

from core.settings import DEBUG
import logging

logger = logging.getLogger(__name__)

Email = "email"
ValidateKey = "validatekey"
isNicePassDone = "isNicePassDone"
isEmailValidate = "isEmailValidate"


# 회원가입
class UserRegistrationAPIView(generics.GenericAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)
    
    def post(self, request):
        token_version_id = request.data.get("token_version_id")
        if token_version_id:
            cache_data = cache.get(token_version_id)
            if cache_data is None:
                return Response({"message": "token_version_id가 잘못되었습니다."}, status=status.HTTP_400_BAD_REQUEST)
            isNicePassDone = cache_data.get("isNicePassDone")
            isEmailValidate = cache_data.get("isEmailValidate")
            name = cache_data.get("name")
            birthdate = cache_data.get("birthdate")
            gender = cache_data.get("gender")
            nationalinfo = cache_data.get("nationalinfo")
            mobileno = cache_data.get("mobileno")
            email = cache_data.get("email")
        else:
            isNicePassDone = request.session.get(isNicePassDone)
            isEmailValidate = request.session.get(isEmailValidate)
            name = request.session.get("name")
            birthdate = request.session.get("birthdate")
            gender = request.session.get("gender")
            nationalinfo = request.session.get("nationalinfo")
            mobileno = request.session.get("mobileno")
            email = request.session.get("email")
            
        if isNicePassDone != True:
            return Response(
                {"message": "nicepass validation need first"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        # 이메일 인증 여부 확인
        
        
        if isEmailValidate != True:
            print("이메일 인증이 안됨!")
            return Response(
                {"message": "email validation need first"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        # 방제사라면 인증후 직접 바꾸어줌
        if request.data["type"] == 3:
            is_active = False
        else:
            is_active = True
        
        optinal_consent = request.data.get("optinal_consent")

        try:
            serializer = UserRegistrationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(
                name=name,
                birthdate=birthdate,
                gender=gender,
                nationalinfo=nationalinfo,
                mobileno=mobileno,
                email=email,
                is_active=is_active,
                optinal_consent=optinal_consent,
                marketing_agreement_date = now() if optinal_consent else None,
                required_consent_date = now(),
            )

            request.session.flush()  # 세션의 모든 것을 삭제
            cache_data.clear()  # 캐시의 모든 것을 삭제

            response = {
                "success": True,
                "message": "User successfully registered!",
            }
            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


# 이메일과 비밀번호로 로그인
class UserLoginAPIView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            response = {
                "access": serializer.validated_data["access"],
                "refresh": serializer.validated_data["refresh"],
                "user": {
                    "access": serializer.validated_data["access"],
                    "refresh": serializer.validated_data["refresh"],
                    "uuid": serializer.validated_data["uuid"],
                    
                    "name": serializer.validated_data["name"],
                    "birthdate": serializer.validated_data["birthdate"],
                    "gender": serializer.validated_data["gender"],
                    "nationalinfo": serializer.validated_data["nationalinfo"],
                    "mobileno": serializer.validated_data["mobileno"],
                    "email": serializer.validated_data["email"],
                    "type": serializer.validated_data["type"],
                    
                    "road": serializer.validated_data["road"],
                    "jibun": serializer.validated_data["jibun"],
                    "detail": serializer.validated_data["detail"],
                    "is_active": serializer.validated_data["is_active"],
                    "created_at": serializer.validated_data["created_at"],
                    "updated_at": serializer.validated_data["updated_at"],
                    
                    "optinal_consent" : serializer.validated_data["optinal_consent"],
                    "marketing_agreement_date" : serializer.validated_data["marketing_agreement_date"],
                    "required_consent_date" : serializer.validated_data["required_consent_date"],
                    
                    "bank_name": serializer.validated_data["bank_name"],
                    "bank_account_number": serializer.validated_data["bank_account_number"],
                },
            }
            return Response(response, status=status.HTTP_200_OK)

        except AuthenticationFailed as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# 로그아웃
class UserLogoutAPIView(TokenBlacklistView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        response = super().post(request)
        
        if response.status_code == 205:
            response.data = {"message": "Successfully logged out."}
            return Response(response.data, status=status.HTTP_205_RESET_CONTENT)
        else:
            return Response(
                {"error": "Failed to log out."},
                status=status.HTTP_400_BAD_REQUEST,
            )


# 사용자 정보를 수정 - 오직 자기자신의 정보만 수정가능 - access토큰으로 인증
class ProfileAPIView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, OnlyOwnerCanUpdate]

    def get(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        try:
            serializer = self.get_serializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
class UserDeleteView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request):
        user = request.user
        reason = request.data.get("reason")
        
        try:
            refresh_token = request.data.get("refresh_token")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            # user 값을 데이터에 포함하지 않고, 나중에 serializer.save() 시 전달
            serializer_data = {'reason': reason}
            serializer = UserChurnReasonSerializer(data=serializer_data)
            
            if serializer.is_valid():
                # user 값을 명시적으로 할당
                serializer.save(user=user)
                
                user.is_active = False
                user.save()
                return Response({"message": "회원 탈퇴가 완료되었습니다."}, status=status.HTTP_204_NO_CONTENT)
            
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(('POST',))
def emailValidationSend(request):
    try:
        receive_email = request.data.get("email")
        token_version_id = request.data.get("token_version_id")
        # 이메일 유효성 검사
        if not receive_email:
            return Response(
                {"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        # 6자리 인증번호 생성
        validate_key = str(uuid.uuid4().int)[:6]

        # 세션에 이메일과 인증번호 저장
        if token_version_id:
            cache_data = cache.get(token_version_id)
            cache_data["email"] = receive_email
            cache_data["validate_key"] = validate_key
            cache_data["isEmailValidate"] = False
            cache.set(token_version_id, cache_data, timeout=1200)  # 5분동안 캐시에 저장
        else:
            request.session["email"] = receive_email
            request.session["ValidateKey"] = validate_key
            request.session["isEmailValidate"] = False
            request.session.set_expiry(300)  # 5분 후 세션 만료
            request.session.save()

        # 이메일 제목 및 HTML 메시지
        subject = "드론평야 인증번호입니다"
        message = f"""
        <html>
        <body>
            <h2>드론평야 인증번호</h2>
            <p>안녕하세요!</p>
            <h3 style="color:blue;">인증번호: <strong>{validate_key}</strong></h3>
            <p>이 인증번호는 5분 동안 유효합니다.</p>
        </body>
        </html>
        """

        # 이메일 전송
        email = EmailMessage(subject=subject, body=message, to=[receive_email])
        email.content_subtype = "html"
        email.send()

        logger.info(
            f"Verification email sent to {receive_email} (Code: {validate_key})"
        )

        return Response(
            {"message": "Email sent successfully."}, status=status.HTTP_201_CREATED
        )

    except Exception as e:
        return Response(
            {"message": "Failed to send email.", "error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    

@api_view(("POST",))
# @parser_classes((JSONParser,))
def validationCheck(request):
    token_version_id = request.data.get("token_version_id")
    send_validate_key = request.data.get("validate_key")
    try:
        if token_version_id:
            cache_data = cache.get(token_version_id)
            if cache_data is None:
                return Response({"message": "token_version_id error"}, status=status.HTTP_400_BAD_REQUEST)
            validate_key = cache_data.get("validate_key")
        elif request.session.get("ValidateKey"):
            validate_key = request.session.get("ValidateKey")

        if send_validate_key == validate_key:
            if token_version_id:
                cache_data["isEmailValidate"] = True
                cache.set(token_version_id, cache_data, timeout=1200)
                return Response({"message": "email validated"}, status=status.HTTP_200_OK)
            else:
                request.session["isEmailValidate"] = True
                request.session.save()
                return Response({"message": "email validated"}, status=status.HTTP_200_OK)

        else:
            return Response({"message": "validate key error"}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 비밀번호 재설정 - 이메일주소,인증번호,비밀번호 필요
@api_view(["POST"])
@parser_classes([JSONParser])
def password_reset(request):
    try:
        name = request.session.get('name')
        birthdate = request.session.get('birthdate')
        gender = request.session.get('gender')
        nationalinfo = request.session.get('nationalinfo')
        mobileno = request.session.get('mobileno')
        if request.session.get('name') is None:
            return Response({"message": "세션이 만료되었습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        user = CustomUser.objects.filter(
                name=name,
                birthdate=birthdate,
                gender=gender,
                nationalinfo=nationalinfo,
                mobileno=mobileno).first()
        if not user:
            return Response({"message": "가입되지 않은 유저입니다."}, status=status.HTTP_404_NOT_FOUND)
        user.set_password(request.data.get("password"))
        user.save()
        return Response({"message": "비밀번호가 변경되었습니다."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class DeviceSessionView(APIView):
    def get(self, request):
        session_key = request.session.session_key
        
        if not session_key:
            return Response({"status": "error", "message": "Session not found"}, status=404)
        
        session_data = Session.objects.filter(session_key=session_key).first()
        if not session_data:
            return Response({"status": "error", "message": "Session not found"}, status=404)
        
        return Response({"session_key": session_key, "session_data": session_data.get_decoded()}, status=200)
    
    def post(self, request):
        # 요청에서 기기 UUID 가져오기
        device_uuid = request.data.get("device_uuid")

        if not device_uuid:
            return JsonResponse({"status": "error", "message": "Device UUID is required"}, status=400)
        
        # UUID 유효성 검사
        if not self.is_valid_uuid(device_uuid):
            return JsonResponse({"status": "error", "message": "Invalid Device UUID"}, status=400)

        
        # 세션 생성
        session_id = self.create_session(request, device_uuid)

        return JsonResponse({
            "status": "success", 
            "session_id": session_id,
            "device_uuid": device_uuid
            },status=200)

    def is_valid_uuid(self, uuid_string):
        """UUID 형식 유효성 검증"""
        try:
            if len(uuid_string) == 16:
                # 16자리 UUID를 표준 32자리 형식으로 변환
                formatted_uuid = f"{uuid_string[:8]}-{uuid_string[8:12]}-{uuid_string[12:16]}-0000-000000000000"
                print(formatted_uuid)
                uuid.UUID(formatted_uuid, version=4)
            else:
                uuid.UUID(uuid_string, version=4)
            return True
        except Exception as e:
            print(e)
            return False

    def create_session(self, request, device_uuid):
        # 동일한 UUID로 기존 세션 확인
        existing_session = Session.objects.filter(session_key=request.session.session_key).first()
        print(existing_session)
        if existing_session:
            return request.session.session_key

        # 새 세션 생성
        request.session['device_uuid'] = device_uuid
        request.session.save()
        return request.session.session_key

#아이디찾기
@api_view(['POST'])
def find_id(request):
    try:
        name = request.session.get('name')
        birthdate = request.session.get('birthdate')
        gender = request.session.get('gender')
        nationalinfo = request.session.get('nationalinfo')
        mobileno = request.session.get('mobileno')

        if request.session.get('name') is None:
            return Response({"message": "세션이 만료되었습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        
        user = CustomUser.objects.filter(
            name=name,
            birthdate=birthdate, 
            gender=gender,
            nationalinfo=nationalinfo, 
            mobileno=mobileno).first()
        
        
        if not user:
            return Response({"message": "가입되지 않은 유저입니다."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"email": user.email}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class BankAccountAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            serializer = BankAccountSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def get(self, request):
        queryset = BankAccount.objects.filter(owner=request.user)
        serializer = BankAccountSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def delete(self, request):
        try:
            account = BankAccount.objects.get(uuid=request.data.get("uuid"))
            account.delete()
            return Response({"message": "계좌 삭제 완료"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def patch(self, request):
        try:
            account = BankAccount.objects.get(uuid=request.data.get("uuid"))
            serializer = BankAccountSerializer(account, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    

import os
from django.http import Http404
from django.conf import settings
from django.http import FileResponse

def terms_of_service(request, id):
    file_path = os.path.join(settings.BASE_DIR, f"templates/register{id}_structure_modified.html")
    
    try:
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=f"register{id}.html")
    except FileNotFoundError:
        raise Http404("이용약관 파일을 찾을 수 없습니다.")