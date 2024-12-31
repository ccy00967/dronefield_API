from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import (
    niceCrytoToken,
    getNicePassUserData,
    emailValidationSend,
    validationCheck,
    passwordReset,
)

'''
1. 이메일, 패스워드로 로그인
-> 리프레시토큰, 액세스토큰 발급
2. 리프레시토큰으로 로그인
-> 액세스토큰 발급
'''

urlpatterns = [
    # 토큰을 아예 발급받는다? 이것은 일단 막아두기
    #path('token/obtain/', CustomTokenObtainPairView.as_view(), name='token_create'),
    # 리프레시토큰으로 액세스토큰 발급받기
    path('accesstokenlogin/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    
    # 나이스 표준창 호출하기
    path('callnicepass/', niceCrytoToken),

    # 나이스 본인 인증정보 받기
    path('nicepasscallback/', getNicePassUserData), 

    # 이메일 전송
    path('emailsend/', emailValidationSend), 

    # 인증번호 인증
    path('validatekeycheck/', validationCheck), 

    # 비밀번호 재설정
    path('passwordreset/', passwordReset),

]
