from django.urls import path
from exterminator import views

urlpatterns = [
    # 방제사 생성
    path(
        "exterminator/",
        views.ExterminatorView.as_view(),
        name=views.ExterminatorView.name,
    ),
    # 방제사 조회
    path(
        "exterminator/<uuid:uuid>",
        views.ExterminatorView.as_view(),
        name=views.ExterminatorView.name,
    ),
    # 방제사 라이센스 수정
    path(
        "license/<uuid:uuid>/",
        views.ExterminatorLicenseView.as_view(),
        name=views.ExterminatorLicenseView.name,
    ),
]
