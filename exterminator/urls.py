from django.urls import path
from exterminator import views

urlpatterns = [
    # 신청서에 담당 방제사 등록, 삭제
    path(
        #"accept/<uuid:orderid>/",
        "accept/",
        views.ExterminatorAcceptCreateAPIView.as_view(),
        name=views.ExterminatorAcceptCreateAPIView.name,
    ),
    path(
        "acceptcancel/<uuid:orderid>/",
        views.ExterminatorAcceptUpdateDeleteView.as_view(),
        name=views.ExterminatorAcceptUpdateDeleteView.name,
    ),

    # 방제 신청서 전부 가져오기
    path(
        "getrequests/",
        views.ExterminatorGetRequestsListView.as_view(),
        name=views.ExterminatorGetRequestsListView.name,
    ),

    # 방제 신청서 cd로 전부 가져오기
    path(
        "getrequests/<int:cd>/",
        views.ExterminatorGetRequestsWithCdListView.as_view(),
        name=views.ExterminatorGetRequestsWithCdListView.name,
    ),

    # 담당방제 신청서 가져오기
    path(
        "workinglist/",
        views.ExterminatorGetOwnRequestsListView.as_view(),
        name=views.ExterminatorGetOwnRequestsListView.name,
    ),
    path(
        "workinglist/<int:state>/",
        views.ExterminatorGetOwnRequestsListView.as_view(),
        name=views.ExterminatorGetOwnRequestsListView.name,
    ),

    # 방제상태 업데이트
    path(
        "exterminatestate/<uuid:orderid>/",
        views.ExterminateStateUpdate.as_view(),
        name=views.ExterminateStateUpdate.name,
    ),
]
