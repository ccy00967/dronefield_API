from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from django.conf import settings
from django.core.cache import cache
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
from django.shortcuts import redirect

@api_view(('POST',))
def niceCrytoToken(request):
    """
        url: /user/nice-token/
    """
    base_url = "https://api.dronefield.co.kr"

    #TODO: 리턴 주소 하드 코딩으로 고정시 웹에서 자식창이 닫히질 않음
    #TODO: hmac_key 에러 발생: 세션 정보가 제대로 전달 되지 않아서 생기는 에러
    returnURL = base_url + "/user/nice-callback/"
    #returnURL = request.data["returnURL"]
    
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

    cache_data  = {
        "token_version_id": token_version_id,
        "req_no": req_no,
        "key": key,
        "iv": iv,
        "hmac_key": hmac_key,
    }
    cache.set(token_version_id, cache_data , timeout=1200)# 5분동안 캐시에 저장
    
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
        "integrity_value": integrity_value, 
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
    """
        url: /user/nice-callback/
    """
    try:
        # GET 요청일 때와 POST 요청일 때 모두 파라미터를 가져올 수 있도록 수정
        token_version_id = request.GET.get("token_version_id") or request.data.get("token_version_id")
        enc_data = request.GET.get("enc_data") or request.data.get("enc_data")
        integrity_value = request.GET.get("integrity_value") or request.data.get("integrity_value")
        print(token_version_id)
        print(enc_data)
        print(integrity_value)
        if not token_version_id:
            return Response(
                {"message": "token_version_id가 필요합니다."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cache_data = cache.get(token_version_id)
        
        if not cache_data:
            return Response(
                {"message": f"해당 token_version_id:{token_version_id}에 대한 캐시 데이터가 없습니다."}, 
                status=400
            )
        
        # 캐시 데이터에서 필요한 값 추출
        key = cache_data.get("key")
        iv = cache_data.get("iv")
        hmac_key = cache_data.get("hmac_key")
        req_no = cache_data.get("req_no")
        
        # 필수 데이터가 모두 있는지 확인
        if not all([key, iv, hmac_key, req_no]):
            return Response(
                {"message": "캐시 데이터에 필요한 정보가 부족합니다."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 무결성 검증
        h = hmac.new(
            key=hmac_key.encode(),
            msg=enc_data.encode("utf-8"),
            digestmod=hashlib.sha256
        ).digest()
        integrity = base64.b64encode(h).decode("utf-8")

        if integrity != integrity_value:
            return Response(
                {"message": "무결성 값이 다릅니다. 데이터가 변경된 것이 아닌지 확인 바랍니다."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # 데이터 복호화 (한 번만 호출)
        dec_data = json.loads(decrypt_data(enc_data, key, iv))
        
        # 요청 번호 검증
        if req_no != dec_data.get("requestno"):
            return HttpResponse(
                '<script type="text/javascript">window.close();</script>', 
                status=400
            )
        
        # 필요한 데이터 추출 및 캐시 업데이트
        cache_data["name"] = dec_data.get("name")
        cache_data["birthdate"] = dec_data.get("birthdate")
        cache_data["gender"] = dec_data.get("gender")
        cache_data["nationalinfo"] = dec_data.get("nationalinfo")
        cache_data["mobileno"] = dec_data.get("mobileno")
        cache_data["isNicePassDone"] = True
        cache.set(token_version_id, cache_data, timeout=1200)  # 5분동안 캐시에 저장

        # 세션 업데이트 (선택 사항)
        request.session["name"] = dec_data.get("name")
        request.session["birthdate"] = dec_data.get("birthdate")
        request.session["gender"] = dec_data.get("gender")
        request.session["nationalinfo"] = dec_data.get("nationalinfo")
        request.session["mobileno"] = dec_data.get("mobileno")
        request.session["isNicePassDone"] = True
        request.session.save() 

        # 리다이렉션 URL 설정 (프론트엔드 URL 또는 모바일 딥 링크)
        # frontend_url = "https://yourfrontend.com/auth-success/"  # 실제 프론트엔드 URL로 변경
        # params = {'token_version_id': token_version_id}
        # redirect_url = f"{frontend_url}?{urlencode(params)}"
    
        # return redirect(redirect_url)
        
        return redirect("<script type='text/javascript'>window.close();</script>")
        
    except Exception as e:
        return Response(
            {"message": f"에러 발생: {e}"}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    
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