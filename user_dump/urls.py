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
   
    
]
