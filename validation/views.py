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

from drf_yasg.utils import swagger_auto_schema
from . import swagger_doc

from .nice_fuc import encrypt_data
from .nice_fuc import decrypt_data
from .nice_fuc import clientID
from .nice_fuc import secretKey
from .nice_fuc import APIUrl
from .nice_fuc import productID
from .nice_fuc import access_token
#from .nice_fuc import returnURL
from user.models import CustomUser


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


# 일반 api에 달기
# 인증 이메일 발송 인증번호를 포함
@swagger_auto_schema(
    method="POST",
    operation_id='인증번호 발송',
    operation_description='유저 이메일 인증번호 발송',
    request_body=swagger_doc.EmailRequest,
    responses=swagger_doc.EmailResponse,
)
@api_view(('POST',))
#@parser_classes((JSONParser,))
def emailValidationSend(request):
    if request.method == 'POST':
        validatekey = str(uuid.uuid1().int)[0:6] #uuid 랜덤값 생성(만약 문자열이라면 str)

        reciveEmail = request.data["email"]

        request.session[Email] = reciveEmail # 인증할 이메일을 세션에 저장
        request.session[ValidateKey] = validatekey
        request.session.save() # 위 세션 저장

        subject = "드론평야 인증번호입니다"	# 타이틀
        to = [reciveEmail]                  # 수신할 이메일 주소
        # html파일은 client에 존재함
        message = render_to_string('emailvalidation.html', {
                    'validatekey': validatekey,
                })
        EmailMessage(subject=subject, body=message, to=to).send()

        return Response({"message": "email sended"}, status = status.HTTP_201_CREATED)
    
    return Response({"message": "email send error"}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)


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
            # 이메일 인증성공 - 회원가입에서 확인할 값
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
@api_view(('POST',))
@parser_classes((JSONParser,))
def passwordReset(request) :
    if request.method == 'POST':
        if(request.session.get(ValidateKey) == request.data[ValidateKey]):
            user = CustomUser.objects.get(email=request.data["email"])
            user.set_password(raw_password=request.data["password"])
            user.save()  
            return Response({"message": "password updated"}, status = status.HTTP_200_OK)
        else:
            return Response({"message": "validate key error"}, status = status.HTTP_401_UNAUTHORIZED)
