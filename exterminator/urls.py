from django.urls import path
from exterminator import views

urlpatterns = [
    
    # 방제사 자격증
    path("licenses/", views.ExterminatorLicenseListView.as_view(), name=views.ExterminatorLicenseListView.name),
    path("license/", views.ExterminatorLicenseCreateView.as_view(), name=views.ExterminatorLicenseCreateView.name),
    path("license/<uuid:uuid>/", views.ExterminatorLicenseDetailView.as_view(), name=views.ExterminatorLicenseDetailView.name),
    #path("<uuid:uuid>/", views.ExterminatorView.as_view(), name=views.ExterminatorView.name),
    # 방제사 라이센스 수정
   
]
