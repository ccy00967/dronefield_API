from django.urls import path
from payments import views

urlpatterns = [
    # 결제 완료 요청
    path(
        "success/",
        views.TossPaymentsUpdateDeleteWithRequestView.as_view(),
        name=views.TossPaymentsUpdateDeleteWithRequestView.name,
    ),
    # 결제 취소 요청
    path(
        "cancel/<uuid:orderid>/",
        views.TossPaymentsUpdateDeleteView.as_view(),
        name=views.TossPaymentsUpdateDeleteView.name,
    ),
]
