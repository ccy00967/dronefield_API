from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from django.conf import settings
import requests
import base64
import hashlib
import hmac
import json
import random
import time
from datetime import datetime
from urllib.parse import urlencode
from django.contrib.sessions.models import Session
from .utils import (encrypt_data, decrypt_data, clientID, secretKey, APIUrl, productID, access_token, isNicePassDone)


@api_view(('POST',))
def niceCrytoToken(request):
    base_url = "https://api.dronefield.co.kr"
    returnURL = base_url + "/user/nice-callback/"
    
    # 나이스 토큰 요청
    now = str(int(time.time()))
    req_dtim = datetime.now().strftime("%Y%m%d%H%M%S")
    req_no = "REQ" + req_dtim + str(random.randint(0, 10000)).zfill(4)
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

    # print("=====================================")
    # print(response.json())
    # print(response.json()["dataBody"])
    # print("=====================================")
    
    #응답 받은 데이터 암호화
    sitecode = response.json()["dataBody"]["site_code"]
    token_version_id = response.json()["dataBody"]["token_version_id"]
    token_val = response.json()["dataBody"]["token_val"]
    result = req_dtim + req_no + token_val
    resultVal = base64.b64encode(hashlib.sha256(result.encode()).digest()).decode("utf-8")
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
        key=hmac_key.encode(),
        msg=enc_data.encode("utf-8"),
        digestmod=hashlib.sha256
        ).digest()
    
    integrity_value = base64.b64encode(h).decode("utf-8")

    # 세션에 저장
    request.session["token_version_id"] = token_version_id
    request.session["req_no"] = req_no
    request.session["key"] = key
    request.session["iv"] = iv
    request.session["hmac_key"] = hmac_key
    request.session.save() # 위 세션 저장
    
    # 나이스창 호출 url 생성
    base_url = "https://nice.checkplus.co.kr/CheckPlusSafeModel/checkplus.cb"
    base_data = {
        "m": "service",
        "token_version_id": token_version_id,
        "enc_data": enc_data,
        "integrity_value": integrity_value
    }
    response_url = f"{base_url}?{urlencode(base_data)}"
    
    return Response({
        "token_version_id": token_version_id,
        "enc_data" : enc_data,
        "integrity_value" : integrity_value,
        "url" : response_url
    }, status = status.HTTP_200_OK)



@api_view(('POST','GET'))
def getNicePassUserData(request):
    try:
        token_version_id = request.GET.get("token_version_id")
        enc_data = request.GET.get("enc_data")
        integrity_value = request.GET.get("integrity_value")
        session_id = request.COOKIES.get("sessionid")
    
        session = Session.objects.get(session_key=session_id)
        session_data = session.get_decoded()
        key = session_data.get("key")
        iv = session_data.get("iv")
        hmac_key = session_data.get("hmac_key")
        req_no = session_data.get("req_no")
    except Session.DoesNotExist:
        return Response({"message": "세션값이 존재하지 않습니다."}, status = status.HTTP_400_BAD_REQUEST)
     
    h = hmac.new(
        key=hmac_key.encode(),
        msg=enc_data.encode("utf-8"),
        digestmod=hashlib.sha256
        ).digest()
    integrity = base64.b64encode(h).decode("utf-8")

    if integrity != integrity_value:
        return Response({"message": "무결성 값이 다릅니다. 데이터가 변경된 것이 아닌지 확인 바랍니다."}, status = status.HTTP_400_BAD_REQUEST)

    dec_data = json.loads(decrypt_data(enc_data, key, iv))
    
    if req_no != dec_data["requestno"]:
        return HttpResponse('<script type="text/javascript">'+ 'window.close();' + '</script>', status = status.HTTP_400_BAD_REQUEST)
    
    
    try:
        dec_data = json.loads(decrypt_data(enc_data, key, iv))

        request.session["name"] = dec_data["name"]
        request.session["birthdate"] = dec_data["birthdate"]
        request.session["gender"] = dec_data["gender"]
        request.session["nationalinfo"] = dec_data["nationalinfo"]
        request.session["mobileno"] = dec_data["mobileno"]
        request.session[isNicePassDone] = True
        request.session.save() 

        return HttpResponse('<script type="text/javascript">'+ 'window.close();' + '</script>', status = status.HTTP_200_OK)
    
    except Exception as e:
        return Response({"message": f"에러 발생: {e}"}, status = status.HTTP_400_BAD_REQUEST)
    
def get_nice_form(request):
    return render(request, 'nice.html')  
def nice_auth_view(request):
    return render(request, "nice_auth.html", {})

def flutter_nice_auth_view(request):
    return render(request, "flutter_nice_auth.html", {})


from django.contrib.sessions.models import Session
from django.utils import timezone

def view_session_data(request, session_key):
    # 세션 키를 사용하여 해당 세션 객체 조회
    try:
        session = Session.objects.get(session_key=session_key, expire_date__gt=timezone.now())
        session_data = session.get_decoded()  # 세션 데이터 디코드
        return HttpResponse(f"All session data: {session_data}")
    except Session.DoesNotExist:
        return HttpResponse("Session not found or expired")