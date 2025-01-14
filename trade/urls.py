from django.urls import path
from trade import views


urlpatterns = [
    # 신청서 등록 - 농지정보 필요
    path("<uuid:landuuid>/", views.RequestCreateAPIView.as_view(), name=views.RequestCreateAPIView.name),
    # 농민용 본인 신청서 목록 가져오기
    path("list/", views.FarmerRequestListAPIView.as_view(), name=views.FarmerRequestListAPIView.name),
    path("counts/", views.count_by_exterminateState, name="state_count"),
    # 방제사용 신청서 목록 가져오기 - cd값 필요
    path("lists/", views.ExterminatorRequestListAPIView.as_view(), name=views.ExterminatorRequestListAPIView.name),
    # 방제사용 신청서 본인 담당 목록 가져오기
    path("work-list/", views.ExterminatorWorkRequestListAPIView.as_view(), name=views.ExterminatorWorkRequestListAPIView.name),
    # 신청서 읽기, 수정, 삭제
    path("detail/<uuid:orderId>/", views.RequestListUpdateDeleteView.as_view(), name=views.RequestListUpdateDeleteView.name),
    #TODO: 농민의 신청서 상태 업데이트: checkState (방제 완료 최종 확인)
    #TODO: 방제사의 신청서 상태 업데이트: exterminateState (작업 상태 업데이트)
]
