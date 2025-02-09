from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import (
    #niceCryptoToken,
    emailValidationSend,
    validationCheck,
    password_reset,
    #niceCallback,
    terms_of_service,
    BankAccountAPIView
)

from .service.Nice.views import (
    niceCrytoToken,
    getNicePassUserData,
    nice_auth_view,
    flutter_nice_auth_view,
    view_session_data
)

from .service.SMS.views import (
    find_id_sendcode,
    find_id_checkcode,
    reset_password_sendcode,
    reset_password_checkcode,
    reset_password_confirm
)

from .views import (
    UserRegistrationAPIView,
    UserLoginAPIView,
    UserLogoutAPIView,
    ProfileAPIView,
    DeviceSessionView,
    UserDeleteView,
    find_id
)

urlpatterns = [
    path("refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),  # 리프레시토큰으로 액세스토큰 발급받기
    path("login/", UserLoginAPIView.as_view(), name="login"),  # 로그인하기
    path("logout/", UserLogoutAPIView.as_view(), name="logout"),  # 로그아웃하기
    path("register/", UserRegistrationAPIView.as_view(), name="register"),  # 회원가입하기
    path("profile/", ProfileAPIView.as_view(), name="userdataupdate"),  # 자신의 정보 읽기, 수정
    path("validatekey/", emailValidationSend, name="validatekey"),  # 이메일로 인증번호 전송
    path("validatekeycheck/", validationCheck, name= "validatecheck"),  # 인증번호 인증
    path("passwordreset/", password_reset, name="passwordreset"),  # 비밀번호 재설정
    path("delete/", UserDeleteView.as_view(), name="delete"),  # 회원탈퇴
    
     #아이디 찾기
    #path("passwordreset/", send_sms, name="passwordreset"),  # 비밀번호 재설정
    path("findid/sendcode/", find_id_sendcode, name="findid_sendcode"),
    path("findid/checkcode/", find_id_checkcode, name="findid_checkcode"),  # 아이디 찾기
    path("resetpassword/sendcode/", reset_password_sendcode, name="resetpassword_sendcode"),
    path("resetpassword/checkcode/", reset_password_checkcode, name="resetpassword_checkcode"),
    path("resetpassword/confirm/", reset_password_confirm, name="resetpassword_confirm"),  # 비밀번호 재설정
    
    
    #나이스
    path("nice-token/", niceCrytoToken),  # 나이스 표준창 호출하기
    path("nice-callback/", getNicePassUserData),  # 나이스 콜백
    path("nice-auth/", nice_auth_view, name="nice-auth"),
    path("flutter/nice-auth/", flutter_nice_auth_view, name="nice-auth"),
    #이용약관
    path("term/<int:id>/", terms_of_service, name="terms"),  # 이용약관
    
    #자신의 계좌
    path("bankaccount/", BankAccountAPIView.as_view(), name="bankaccount"),  # 계좌 등록, 읽기, 수정, 삭제제
    
    #세션
    path("session/", DeviceSessionView.as_view(), name="session"),  # 세션 생성
    #path("sessioncheck/", view_session_data, name="sessioncheck"),  # 세션 체크
    # FIX : 미사용
    # path('manager/users/', ManageUserListView.as_view(), name='manage_get_users'),
    # path('manager/<uuid:uuid>/', ManageUserRetrieveUpdateDestroyView.as_view(), name='manage_update_users'),
    # path('manager/exterminator/<uuid:uuid>/', ManageExterminatorRetrieveUpdateDestroyView.as_view(), name='manage_update_exterminator'),
    # path('userinfo/exterminator/<uuid:uuid>/', ExterminatorView.as_view(), name='get_exterminator_info'),
    # path('accesstokenlogin/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),# 리프레시토큰으로 액세스토큰 발급받기
    # path('token/obtain/', CustomTokenObtainPairView.as_view(), name='token_create'),# 토큰을 아예 발급받는다? 이것은 일단 막아두기
]
