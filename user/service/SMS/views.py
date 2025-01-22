import requests
import json
from django.shortcuts import render
from rest_framework.decorators import api_view
from core.settings import ALIGO_ACCESS_ID, ALIGO_ACCESS_KEY, ALIGO_SENDER
from user.models import CustomUser
from rest_framework.response import Response
from rest_framework import status
import uuid


send_url = "https://apis.aligo.in/send/"  # 요청을 던지는 URL, 현재는 문자보내기

# ================================================================== 문자 보낼 때 필수 key값
# API key, userid, sender, receiver, msg
# API키, 알리고 사이트 아이디, 발신번호, 수신번호, 문자내용


@api_view(("POST",))
def find_id_sendcode(request):
    data = request.data
    name = request.data.get("name")
    birthdate = request.data.get("birthdate")
    mobileno = request.data.get("mobileno")

    user = CustomUser.objects.filter(
        name=name, birthdate=birthdate, mobileno=mobileno
    ).first()

    if user is None:
        return Response(
            {"message": "일치하는 정보가 없습니다."}, status=status.HTTP_404_NOT_FOUND
        )

    validate_key = str(uuid.uuid4().int)[:6]
    
    request.session["validate_key"] = validate_key
    request.session["name"] = name
    request.session["birthdate"] = birthdate
    request.session["mobileno"] = mobileno
    request.session.set_expiry(180)
    request.session.save()
    
    
    title = "드론평야 인증번호입니다"
    message = f"""드론평야 인증번호 입니다.\n인증번호: [{validate_key}]\n이 인증번호는 5분 동안 유효합니다."""
    
    sms_data = {
        "key": ALIGO_ACCESS_KEY,  #
        "userid": ALIGO_ACCESS_ID,  # 알리고 사이트 아이디
        "sender": ALIGO_SENDER,  # 발신번호
        "receiver": mobileno,  # 수신번호 (,활용하여 1000명까지 추가 가능)
        "msg": message,  # 문자 내용
        "msg_type": "SMS",  # 메세지 타입 (SMS, LMS)
        "title": title,  # 메세지 제목 (장문에 적용)
        "destination": f"{mobileno}|{name}",  # %고객명% 치환용 입력
        #'rdate' : '예약날짜',W
        #'rtime' : '예약시간',
        "testmode_yn": "N",  # 테스트모드 적용 여부 Y/N
    }
    response = requests.post(send_url, data=sms_data)
    return Response(data=response.json(), status=status.HTTP_200_OK)

@api_view(("POST",))
def find_id_checkcode(request):
    validate_key = request.data.get("validate_key")
    if validate_key == request.session["validate_key"]:
        user = CustomUser.objects.filter(
            name=request.session["name"],
            birthdate=request.session["birthdate"],
            mobileno=request.session["mobileno"],
        ).first()
        return Response(
            {"message": "인증번호가 일치합니다.", "id": user.email}, status=status.HTTP_200_OK
        )
    else:
        return Response(
            {"message": "인증번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST
        )

@api_view(("POST",))
def reset_password_sendcode(request):
    data = request.data
    email = request.data.get("email")
    name = request.data.get("name")
    birthdate = request.data.get("birthdate")
    mobileno = request.data.get("mobileno")

    user = CustomUser.objects.filter(email=email).first()

    if user is None:
        return Response(
            {"message": "일치하는 정보가 없습니다."}, status=status.HTTP_404_NOT_FOUND
        )

    validate_key = str(uuid.uuid4().int)[:6]
    
    request.session["validate_key"] = validate_key
    request.session["email"] = email
    request.session["name"] = name
    request.session["birthdate"] = birthdate
    request.session["mobileno"] = mobileno
    request.session.set_expiry(180)
    request.session.save()
    
    
    title = "드론평야 인증번호입니다"
    message = f"""드론평야 인증번호 입니다.\n인증번호: [{validate_key}]\n이 인증번호는 5분 동안 유효합니다."""
    
    sms_data = {
        "key": ALIGO_ACCESS_KEY,  #
        "userid": ALIGO_ACCESS_ID,  # 알리고 사이트 아이디
        "sender": ALIGO_SENDER,  # 발신번호
        "receiver": mobileno,  # 수신번호 (,활용하여 1000명까지 추가 가능)
        "msg": message,  # 문자 내용
        "msg_type": "SMS",  # 메세지 타입 (SMS, LMS)
        "title": title,  # 메세지 제목 (장문에 적용)
        "destination": f"{mobileno}|{name}",  # %고객명% 치환용 입력
        #'rdate' : '예약날짜',W
        #'rtime' : '예약시간',
        "testmode_yn": "N",  # 테스트모드 적용 여부 Y/N
    }
    response = requests.post(send_url, data=sms_data)
    return Response(data=response.json(), status=status.HTTP_200_OK)

@api_view(("POST",))
def reset_password_checkcode(request):
    validate_key = request.data.get("validate_key")
    if validate_key == request.session["validate_key"]:
        email = request.session["email"]
        password = request.data.get("password")
        try:
            user = CustomUser.objects.filter(email=email).first()
            user.set_password(password)
            return Response(
                {"message": "비밀번호가 변경되었습니다."}, status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"message": "비밀번호 변경에 실패했습니다."}, status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(
            {"message": "인증번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST
        )
    
    
    