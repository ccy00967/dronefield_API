from django.urls import path
from .views import NoticeCreateView, NoticeListView, NoticeDetailView, AlarmCreateView, AlarmListView, AlarmDetailView
from .views import get_polygon_api
urlpatterns = [
    
    path("notices/", NoticeListView.as_view(), name=NoticeListView.name),
    path("notice/", NoticeCreateView.as_view(), name=NoticeCreateView.name),
    path("notice/<uuid:uuid>/", NoticeDetailView.as_view(), name=NoticeDetailView.name),
    
    path("alarms/", AlarmListView.as_view(), name=AlarmListView.name),
    path("alarm/", AlarmCreateView.as_view(), name=AlarmCreateView.name),
    path("alarm/<uuid:uuid>/", AlarmDetailView.as_view(), name=AlarmDetailView.name),
    
    path("polygon/", get_polygon_api, name="get_polygon_api"),
]
