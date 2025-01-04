from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import (niceCryptoToken,emailValidationSend,
                    validationCheck,password_reset,
                    niceCallback)

from .views import (UserRegistrationAPIView,UserLoginAPIView,
                    ProfileAPIView,)


'''
1. 이메일, 패스워드로 로그인
-> 리프레시토큰, 액세스토큰 발급
2. 리프레시토큰으로 로그인
-> 액세스토큰 발급
'''

urlpatterns = [
    path('refreshtoken/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),# 리프레시토큰으로 액세스토큰 발급받기
    path('login/', UserLoginAPIView.as_view(), name='login'),# 로그인하기
    path('logout/', jwt_views.TokenBlacklistView .as_view(), name='logout'),# 로그아웃하기
    path('register/', UserRegistrationAPIView.as_view(), name='register'),# 회원가입하기
    path('profile/', ProfileAPIView.as_view(), name='userdataupdate'),# 자신의 정보 읽기, 수정
    
    path('emailsend/', emailValidationSend), # 이메일 전송
    path('validatekeycheck/', validationCheck), # 인증번호 인증
    path('passwordreset/', password_reset), # 비밀번호 재설정
    
    path('nice-token/', niceCryptoToken), # 나이스 표준창 호출하기
    path('nice-callback/', niceCallback), # 나이스 콜백
    
    # FIX : 미사용
    #path('manager/users/', ManageUserListView.as_view(), name='manage_get_users'),
    #path('manager/<uuid:uuid>/', ManageUserRetrieveUpdateDestroyView.as_view(), name='manage_update_users'),
    #path('manager/exterminator/<uuid:uuid>/', ManageExterminatorRetrieveUpdateDestroyView.as_view(), name='manage_update_exterminator'),
    #path('userinfo/exterminator/<uuid:uuid>/', ExterminatorView.as_view(), name='get_exterminator_info'),
    #path('accesstokenlogin/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),# 리프레시토큰으로 액세스토큰 발급받기
    #path('token/obtain/', CustomTokenObtainPairView.as_view(), name='token_create'),# 토큰을 아예 발급받는다? 이것은 일단 막아두기

]
