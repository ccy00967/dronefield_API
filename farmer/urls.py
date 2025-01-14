from django.urls import path
from farmer import views
from rest_framework_simplejwt import views as jwt_views
from .views import TotalLandAreaAPIView

urlpatterns = [
    path("lands/",views.FarmInfoListView.as_view(),name=views.FarmInfoListView.name,), # 농지등록, 목록 가져오기
    path("land/",views.FarmInfoCreateView.as_view(),name=views.FarmInfoCreateView.name,), # 농지정보 생성하기
    path('land/total-area/', TotalLandAreaAPIView.as_view(), name='total-land-area'),#TODO: 농지 총 면적 lands에 추가
    path("land/<uuid:uuid>/",views.FarmInfoAPIView.as_view(),name=views.FarmInfoAPIView.name), # 농지 
]
