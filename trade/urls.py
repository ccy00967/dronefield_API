from django.urls import path
from trade import views

urlpatterns = [
    # 신청서 등록 - 농지정보 필요
    path(
        "/<uuid:landuuid>/",
        # "sendrequest/",
        views.RequestCreateAPIView.as_view(),
        name=views.RequestCreateAPIView.name,
    ),
    # 본인 신청서 목록 가져오기 - 유저 uuid필요
    path(
        "/",
        views.RequestListAPIView.as_view(),
        name=views.RequestListAPIView.name,
    ),
    # 신청서 읽기, 수정, 삭제
    path(
        "/<uuid:orderid>/",
        views.RequestListUpdateDeleteView.as_view(),
        name=views.RequestListUpdateDeleteView.name,
    ),
]
