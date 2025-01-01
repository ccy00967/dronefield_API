from django.urls import path
from trade import views

urlpatterns = [
    # 신청서 등록 - 농지정보 필요
    path(
        "send/<uuid:landuuid>/",
        #"sendrequest/",
        views.CustomerRequestCreateAPIView.as_view(),
        #name=views.CustomerRequestListCreateAPIView.name,
    ),

    # 본인 신청서 목록 가져오기 - 유저 uuid필요
    path(
        "requests/",
        views.CustomerRequestListAPIView.as_view(),
        #name=views.CustomerRequestListCreateAPIView.name,
    ),
    
    # 신청서 읽기, 수정, 삭제
    path(
        "<uuid:orderid>/",
        views.CustomerRequestListUpdateDeleteView.as_view(),
        name=views.CustomerRequestListUpdateDeleteView.name,
    ),

]
