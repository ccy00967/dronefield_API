from django.urls import path
from exterminator import views
from .views import ExterminatorLicenseImageView, DroneCreateAPIView, DroneDetailAPIView, DroneListAPIView

urlpatterns = [
    
    # 방제사 자격증
    path("licenses/", views.ExterminatorLicenseListView.as_view(), name=views.ExterminatorLicenseListView.name),
    path("license/", views.ExterminatorLicenseCreateView.as_view(), name=views.ExterminatorLicenseCreateView.name),
    path("license/<uuid:uuid>/", views.ExterminatorLicenseDetailView.as_view(), name=views.ExterminatorLicenseDetailView.name),
    
    # 방제사 자격증 이미지
    path("license/<uuid:uuid>/image/<str:image_type>/",
        ExterminatorLicenseImageView.as_view(),
        name='exterminator-license-image'
    ),
    
    # 드론
    path("drones/", views.DroneListAPIView.as_view(), name=views.DroneListAPIView.name),
    path("drone/", views.DroneCreateAPIView.as_view(), name=views.DroneCreateAPIView.name),
    path("drone/<uuid:uuid>/", views.DroneDetailAPIView.as_view(), name=views.DroneDetailAPIView.name),
    path("drone/<uuid:uuid>/image/", views.DroneImageView.as_view(), name=views.DroneImageView.name),
]
