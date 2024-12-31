from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from .views import (
    UserRegistrationView,
    UserLoginView,
    UserDataUpdateView,
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
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    # 로그인하기
    path('login/', UserLoginView.as_view(), name='login'),
    # 회원가입하기
    path('register/', UserRegistrationView.as_view(), name='register'),

    # 해당 유저가 자신의 정보 읽기, 수정
    path('userinfo/<uuid:uuid>/', UserDataUpdateView.as_view(), name='userdataupdate'),
    #path('userinfo/exterminator/<uuid:uuid>/', ExterminatorView.as_view(), name='get_exterminator_info'),

    # 관리자용(role:2) - 유저정보 검색,수정,삭제
    #path('manager/users/', ManageUserListView.as_view(), name='manage_get_users'),
    #path('manager/<uuid:uuid>/', ManageUserRetrieveUpdateDestroyView.as_view(), name='manage_update_users'),
    #path('manager/exterminator/<uuid:uuid>/', ManageExterminatorRetrieveUpdateDestroyView.as_view(), name='manage_update_exterminator'),
    
]
