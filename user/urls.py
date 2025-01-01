from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import (niceCrytoToken,getNicePassUserData,
                    emailValidationSend,validationCheck,
                    passwordReset,)

from .views import (UserRegistrationView,UserLoginView,
                    UserDataUpdateView,)


'''
1. 이메일, 패스워드로 로그인
-> 리프레시토큰, 액세스토큰 발급
2. 리프레시토큰으로 로그인
-> 액세스토큰 발급
'''

urlpatterns = [
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),# 리프레시토큰으로 액세스토큰 발급받기
    path('login/', UserLoginView.as_view(), name='login'),# 로그인하기
    path('register/', UserRegistrationView.as_view(), name='register'),# 회원가입하기
    path('userinfo/<uuid:uuid>/', UserDataUpdateView.as_view(), name='userdataupdate'),# 해당 유저가 자신의 정보 읽기, 수정
    #path('userinfo/exterminator/<uuid:uuid>/', ExterminatorView.as_view(), name='get_exterminator_info'),
    
    # 관리자용(role:2) - 유저정보 검색,수정,삭제
    #path('manager/users/', ManageUserListView.as_view(), name='manage_get_users'),
    #path('manager/<uuid:uuid>/', ManageUserRetrieveUpdateDestroyView.as_view(), name='manage_update_users'),
    #path('manager/exterminator/<uuid:uuid>/', ManageExterminatorRetrieveUpdateDestroyView.as_view(), name='manage_update_exterminator'),
    
    
    # 토큰을 아예 발급받는다? 이것은 일단 막아두기
    #path('token/obtain/', CustomTokenObtainPairView.as_view(), name='token_create'),
    path('accesstokenlogin/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),# 리프레시토큰으로 액세스토큰 발급받기
    path('callnicepass/', niceCrytoToken), # 나이스 표준창 호출하기
    path('nicepasscallback/', getNicePassUserData),  # 나이스 본인 인증정보 받기
    path('emailsend/', emailValidationSend), # 이메일 전송
    path('validatekeycheck/', validationCheck), # 인증번호 인증
    path('passwordreset/', passwordReset), # 비밀번호 재설정

]
