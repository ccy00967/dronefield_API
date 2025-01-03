import base64, requests, time, random, json, hashlib, hmac
from datetime import datetime
from Crypto.Cipher import AES
import uuid
from rest_framework import status
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated

from drf_yasg.utils import swagger_auto_schema
from . import swagger_doc
from rest_framework.permissions import AllowAny

from common.nice_fuc import encrypt_data
from common.nice_fuc import decrypt_data
from common.nice_fuc import clientID
from common.nice_fuc import secretKey
from common.nice_fuc import APIUrl
from common.nice_fuc import productID
from common.nice_fuc import access_token
#from .nice_fuc import returnURL
from user.models import CustomUser
from .permissions import OnlyOwnerCanUpdate
from rest_framework import generics
from exterminator.models import Exterminator
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from user.serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer, 
    ProfileSerializer,
    CustomTokenObtainPairSerializer,
    ManageUserListSerializer,
    #ExterminatorSerializer,
)

from core.settings import DEBUG
import logging

logger = logging.getLogger(__name__)

#회원가입
class UserRegistrationAPIView(generics.GenericAPIView):
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
        is_active = True
        if not DEBUG:
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
        
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # 데이터베이스에 유저정보 저장(serializer create실행)
            serializer.save(
                name = request.data.get("name"),
                birthdate = request.data.get("birthdate"),
                gender = request.data.get("gender"),
                nationalinfo = request.data.get("nationalinfo"),
                mobileno = request.data.get("mobileno"),
                email = request.data.get("email"),
                is_active=is_active,
            )
            
            request.session.flush() #세션의 모든 것을 삭제

            response = {
                "success": True,
                "message": "User successfully registered!",
            }
            return Response(response, status=status.HTTP_201_CREATED)

# 이메일과 비밀번호로 로그인
class UserLoginAPIView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        operation_id='로그인',
        operation_description='유저 로그인',
        tags=['user'],
        responses=swagger_doc.UserLoginResponse,
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            response = {
                "access": serializer.validated_data["access"],
                "refresh": serializer.validated_data["refresh"],
                "uuid": serializer.validated_data["uuid"],
            }
            return Response(response, status=status.HTTP_200_OK)
        
        except AuthenticationFailed as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 사용자 정보를 수정 - 오직 자기자신의 정보만 수정가능 - access토큰으로 인증
class ProfileAPIView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, OnlyOwnerCanUpdate]
    
    # @swagger_auto_schema(
    #     operation_id='프로필',
    #     operation_description='유저 프로필',
    #     tags=['user'],
    #     responses=swagger_doc.ProfileResponse,
    # )
    def get(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(request.data)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
 




Email = "email"
ValidateKey = "validatekey"
isNicePassDone = "isNicePassDone"
isEmailValidate = "isEmailValidate"

# 나이스 표준창 호출
@swagger_auto_schema(
    method="POST",
    operation_id='나이스 표준창 호출',
    operation_description='나이스 표준창 호출',
    #request_body=swagger_doc.EmailRequest,
    #responses=swagger_doc.EmailResponse,
)
@api_view(('POST',))
#@parser_classes((JSONParser,))
def niceCrytoToken(request):
    if request.method == 'POST':

        returnURL = request.data["returnURL"]
        
        now = str(int(time.time()))
        req_dtim = datetime.now().strftime("%Y%m%d%H%M%S")
        req_no = "REQ" + req_dtim + str(random.randint(0, 10000)).zfill(4)
        # 요청고유번호(req_no)의 경우 업체 정책에 따라 거래 고유번호 설정 후 사용하면 됩니다.
        # 제공된 값은 예시입니다.

        url = APIUrl + "/digital/niceid/api/v1.0/common/crypto/token"
        auth = access_token + ":" + now + ":" + clientID
        base64_auth = base64.b64encode(auth.encode("utf-8")).decode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "Authorization": "bearer " + base64_auth,
            "productID": productID,
        }
        datas = {
            "dataHeader": {"CNTY_CD": "ko", "TRAN_ID": ""},
            "dataBody": {"req_dtim": req_dtim, "req_no": req_no, "enc_mode": "1"},
        }
        response = requests.post(url, data=json.dumps(datas), headers=headers)
        sitecode = response.json()["dataBody"]["site_code"]
        token_version_id = response.json()["dataBody"]["token_version_id"]
        token_val = response.json()["dataBody"]["token_val"]
        result = req_dtim + req_no + token_val
        resultVal = base64.b64encode(hashlib.sha256(result.encode()).digest()).decode(
            "utf-8"
        )

        key = resultVal[:16]
        iv = resultVal[-16:]
        hmac_key = resultVal[:32]

        plain_data = (
            "{"
            f'"requestno":"{req_no}",'
            f'"returnurl":" {returnURL}",'
            f'"sitecode":"{sitecode}"'
            "}"
        )

        enc_data = encrypt_data(plain_data, key, iv)

        h = hmac.new(
            key=hmac_key.encode(), msg=enc_data.encode("utf-8"), digestmod=hashlib.sha256
        ).digest()
        integrity_value = base64.b64encode(h).decode("utf-8")

        # 인증 완료 후 success페이지에서 사용을 위한 key값은 DB,세션등 업체 정책에 맞춰 관리 후 사용하면 됩니다.
        # 예시에서 사용하는 방법은 세션이며, 세션을 사용할 경우 반드시 인증 완료 후 세션이 유실되지 않고 유지되도록 확인 바랍니다.
        # key, iv, hmac_key 값들은 token_version_id에 따라 동일하게 생성되는 고유값입니다.
        # success페이지에서 token_version_id가 일치하는지 확인 바랍니다.
        request.session["token_version_id"] = token_version_id
        request.session["req_no"] = req_no
        request.session["key"] = key
        request.session["iv"] = iv
        request.session["hmac_key"] = hmac_key
        request.session.save() # 위 세션 저장

        return Response({
            "token_version_id": token_version_id,
            "enc_data" : enc_data,
            "integrity_value" : integrity_value,
        }, status = status.HTTP_200_OK)
        
    return Response({"message": "표준창 호출 실패!"}, status = status.HTTP_404_NOT_FOUND)


# 본인인증 데이터 세션 저장
@swagger_auto_schema(
    method="POST",
    operation_id='본인인증 복호화',
    operation_description='본인인증 데이터 세션저장',
    #request_body=swagger_doc.EmailRequest,
    #responses=swagger_doc.EmailResponse,
)
@api_view(('GET','POST',))
#@parser_classes((JSONParser,))
def getNicePassUserData(request):
    s_token_version_id = request.session.get("token_version_id")
    key = request.session.get("key")
    iv = request.session.get("iv")
    hmac_key = request.session.get("hmac_key")
    req_no = request.session.get("req_no")

    enc_data = ""
    token_version_id = ""
    integrity_value = ""

    # 인증 완료 후 기본적으로 크롬에서는 GET 그 외의 브라우저에서는 POST방식으로 데이터를 전달 하고 있습니다.
    # 업체 서버 설정이 있는 경우 GET/POST 상관 없이 데이터를 전달 받을 수 있는지 확인 바랍니다.
    # 하나의 method로 통일해야 하는 경우 GET으로 설정 가능하며 main페이지에서 plain_data에서 methodtype으로 설정가능합니다. (가이드 확인)
    # 인증 완료 후 전달 드리는 값들이 누락, 유실없이 정상적으로 받고 있는지 확인 바랍니다.
    if request.method == "GET":
        enc_data = request.data["enc_data"]
        token_version_id = request.data["token_version_id"]
        integrity_value = request.data["integrity_value"]
    if request.method == "POST":
        enc_data = request.data["enc_data"]
        token_version_id = request.data["token_version_id"]
        integrity_value = request.data["integrity_value"]

    h = hmac.new(
        key=hmac_key.encode(), msg=enc_data.encode("utf-8"), digestmod=hashlib.sha256
    ).digest()
    integrity = base64.b64encode(h).decode("utf-8")

    if integrity != integrity_value:
        return Response({"message": "무결성 값이 다릅니다. 데이터가 변경된 것이 아닌지 확인 바랍니다."}, status = status.HTTP_404_NOT_FOUND)
    else:
        dec_data = json.loads(decrypt_data(enc_data, key, iv))

        if req_no != dec_data["requestno"]:
            print("세션값이 다릅니다. 올바른 경로로 접근하시기 바랍니다.")
            return HttpResponse('<script type="text/javascript">'
                            + 'window.close();'
                            '</script>')
        else:
            request.session["name"] = dec_data["name"]
            request.session["birthdate"] = dec_data["birthdate"]
            request.session["gender"] = dec_data["gender"]
            request.session["nationalinfo"] = dec_data["nationalinfo"]
            request.session["mobileno"] = dec_data["mobileno"]
            #request.session["mobileco"] = dec_data["mobileco"]

            # 나이스 인증완료 - 회원가입에서 확인할 값
            request.session[isNicePassDone] = True

            request.session.save() # 위 세션 저장

        return Response({
            #"authtype"      : authtype,
            "name"          : dec_data["name"],
            "birthdate"     : dec_data["birthdate"],
            "gender"        : dec_data["gender"],
            "nationalinfo"  : dec_data["nationalinfo"],
            "mobileno"      : dec_data["mobileno"],
            #"mobileco"      : dec_data["mobileco"]
        }, status = status.HTTP_200_OK)


#TODO : SMTP 인증번호 설정 필요
@swagger_auto_schema(
    method="POST",
    operation_id='인증번호 발송',
    operation_description='유저 이메일 인증번호 발송',
    request_body=swagger_doc.EmailRequest,
    responses=swagger_doc.EmailResponse,
)
@api_view(('POST',))
def emailValidationSend(request):
    try:
        receive_email = request.data.get("email")

        # 이메일 유효성 검사
        if not receive_email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        # 6자리 인증번호 생성
        validate_key = str(uuid.uuid4().int)[:6]

        # 세션에 이메일과 인증번호 저장
        request.session["email"] = receive_email
        request.session["validate_key"] = validate_key
        request.session.set_expiry(300)  # 5분 후 세션 만료
        request.session.save()

        # 이메일 제목 및 HTML 메시지
        subject = "드론평야 인증번호입니다"
        message = f"""
        <html>
        <body>
            <h2>드론평야 인증번호</h2>
            <p>안녕하세요!</p>
            <p>비밀번호 재설정을 위해 아래의 인증번호를 입력해주세요.</p>
            <h3 style="color:blue;">인증번호: <strong>{validate_key}</strong></h3>
            <p>이 인증번호는 5분 동안 유효합니다.</p>
        </body>
        </html>
        """

        # 이메일 전송
        email = EmailMessage(subject=subject, body=message, to=[receive_email])
        email.content_subtype = "html"
        email.send()

        logger.info(f"Verification email sent to {receive_email} (Code: {validate_key})")

        return Response({"message": "Email sent successfully."}, status=status.HTTP_201_CREATED)

    except Exception as e:
        logger.error(f"Failed to send email to {receive_email}. Error: {str(e)}")
        return Response(
            {"message": "Failed to send email."},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# 계정 활성화 - 클라이언트에서 "validatekey"로 가져옴
@swagger_auto_schema(
    method="POST",
    operation_id='인증번호 검증',
    operation_description='유저 이메일 인증번호 검증 등등',
    request_body=swagger_doc.ValidateRequest,
    responses=swagger_doc.ValidateResponse,
)
@api_view(('POST',))
#@parser_classes((JSONParser,))
def validationCheck(request) :
    if request.method == 'POST':
        if(request.session.get(ValidateKey) == request.data[ValidateKey]):
            request.session[isEmailValidate] = True
            request.session.save()
            return Response({"message": "email validated"}, status = status.HTTP_200_OK)
        else: 
            return Response({"message": "validate key error"}, status = status.HTTP_401_UNAUTHORIZED)


#비밀번호 재설정 - 이메일주소,인증번호,비밀번호 필요
@swagger_auto_schema(
    method="POST",
    operation_id='비밀번호',
    operation_description='비밀번호 재설정',
    request_body=swagger_doc.PasswordResetRequest,
    responses=swagger_doc.PasswordResetResponse,
)
@api_view(['POST'])
@parser_classes([JSONParser])
def password_reset(request):
    try:
        validate_key = request.session.get("validate_key")  # 세션에서 인증키 가져오기
        if validate_key is None:
            return Response({"message": "Session expired or invalid"}, status=status.HTTP_401_UNAUTHORIZED)

        # 세션의 키와 클라이언트가 보낸 키를 비교
        if validate_key == request.data.get("validate_key"):
            user = CustomUser.objects.filter(email=request.data.get("email")).first()
            if not user:
                return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            # 비밀번호 재설정
            user.set_password(request.data.get("password"))
            user.save()

            # 세션 초기화 (보안 강화)
            request.session.pop("validate_key", None)
            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid validation key"}, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        logger.error(f"Password reset error: {str(e)}")
        return Response({"message": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)