from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import (
    #niceCryptoToken,
    emailValidationSend,
    validationCheck,
    password_reset,
    #niceCallback,
    terms_of_service
)

from common.Nice.views import (
    niceCrytoToken,
    getNicePassUserData,
    get_nice_form
)

from .views import (
    UserRegistrationAPIView,
    UserLoginAPIView,
    ProfileAPIView,
)

urlpatterns = [
    path("refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),  # 리프레시토큰으로 액세스토큰 발급받기
    path("login/", UserLoginAPIView.as_view(), name="login"),  # 로그인하기
    path("logout/", jwt_views.TokenBlacklistView.as_view(), name="logout"),  # 로그아웃하기
    path("register/", UserRegistrationAPIView.as_view(), name="register"),  # 회원가입하기
    path("profile/", ProfileAPIView.as_view(), name="userdataupdate"),  # 자신의 정보 읽기, 수정
    path("validatekey/", emailValidationSend),  # 이메일로 인증번호 전송
    path("validatekeycheck/", validationCheck),  # 인증번호 인증
    path("passwordreset/", password_reset),  # 비밀번호 재설정
    
    #나이스
    path("nice-token/", niceCrytoToken),  # 나이스 표준창 호출하기
    path("nice-form/", get_nice_form),  # 나이스 폼 호출하기
    path("nice-callback/", getNicePassUserData),  # 나이스 콜백
    
    #이용약관
    path("term/<int:id>/", terms_of_service, name="terms"),  # 이용약관
    # FIX : 미사용
    # path('manager/users/', ManageUserListView.as_view(), name='manage_get_users'),
    # path('manager/<uuid:uuid>/', ManageUserRetrieveUpdateDestroyView.as_view(), name='manage_update_users'),
    # path('manager/exterminator/<uuid:uuid>/', ManageExterminatorRetrieveUpdateDestroyView.as_view(), name='manage_update_exterminator'),
    # path('userinfo/exterminator/<uuid:uuid>/', ExterminatorView.as_view(), name='get_exterminator_info'),
    # path('accesstokenlogin/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),# 리프레시토큰으로 액세스토큰 발급받기
    # path('token/obtain/', CustomTokenObtainPairView.as_view(), name='token_create'),# 토큰을 아예 발급받는다? 이것은 일단 막아두기
]
