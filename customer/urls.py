from django.urls import path
from customer import views

urlpatterns = [
    # 농지등록, 목록 가져오기
    path(
        "lands/",
        views.ArableLandInfoListView.as_view(),
        name=views.ArableLandInfoListView.name,
    ),
    # 농지정보 수정, 삭제하기
    path(
        "landinfo/<uuid:uuid>/",
        views.ArableLandInfoRetrieveUpdateDestroyAPIView.as_view(),
        name=views.ArableLandInfoRetrieveUpdateDestroyAPIView.name,
    ),
]
