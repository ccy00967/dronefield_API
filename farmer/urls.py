from django.urls import path
from farmer import views
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    # 농지등록, 목록 가져오기
    path(
        "lands/",
        views.FarmInfoListView.as_view(),
        name=views.FarmInfoListView.name,
    ),
    # 농지정보 수정, 삭제하기
    path(
        "land/",
        views.FarmInfoCreateView.as_view(),
        name=views.FarmInfoCreateView.name,
    ),
    path(
        "land/<uuid:uuid>/",
        views.FarmInfoAPIView.as_view(),
        name=views.FarmInfoListView.name,
    ),
]
