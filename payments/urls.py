from django.urls import path
from payments import views

urlpatterns = [
    # 결제 완료 요청
    path(
        "success/",
        views.RequestTossCreateAPIView.as_view(),
        name=views.RequestTossCreateAPIView.name,
    ),
    # 결제 취소 요청
    path(
        "cancel/",
        views.TossPaymentsUpdateDeleteView.as_view(),
        name=views.TossPaymentsUpdateDeleteView.name,
    ),
    # 결제 정보 가져오기
    path(
        "info/<uuid:tossOrderId>/",
        views.TossPaymentsUpdateDeleteView.as_view(),
        name=views.TossPaymentsUpdateDeleteView.name,
    ),
    # 결제를 건너뛰고 방제사 등록
    path(
        "exterminator-info-upload/",
        views.RequestTossExterminatorCreateAPIView.as_view(),
        name=views.RequestTossExterminatorCreateAPIView.name,
    ),
]
