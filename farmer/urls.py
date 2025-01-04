from django.urls import path
from farmer import views
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    # 농지등록, 목록 가져오기
    path("lands/",views.ArableLandInfoListView.as_view(),name=views.ArableLandInfoListView.name,),
    # 농지정보 수정, 삭제하기
    path("land/",views.ArableLandInfoCreateView.as_view(),name=views.ArableLandInfoCreateView.name,),
    path("land/<uuid:uuid>/",views.ArableLandInfoAPIView.as_view(),name=views.ArableLandInfoListView.name,),
]
