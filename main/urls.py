"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include, re_path

# from django.views.generic import TemplateView

#from drf_yasg.views import get_schema_view
#from drf_yasg import openapi

# ...
'''
schema_view = get_schema_view(
    openapi.Info(
        title="DroneField Django API",
        default_version="version none yet",
        description="Your Swagger Docs descriptions",
        # terms_of_service="https://www.google.com/policies/terms/",
        # contact=openapi.Contact(name="test", email="test@test.com"),
        # license=openapi.License(name="Test License"),
    ),
    public=True,
    # permission_classes=(permissions.AllowAny,),
)
'''

urlpatterns = [
    # path(r'swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    #path(r"swagger",schema_view.with_ui("swagger", cache_timeout=0),name="schema-swagger-ui"),
    #path(r"redoc", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc-v1"),
    path("admin/", admin.site.urls),
    path("user/", include("user.urls")),
    #path("validation/", include("validation.urls")),
    path("farmer/", include("farmer.urls")),
    path("exterminator/", include("exterminator.urls")),
    path("trade/", include("trade.urls")),
    path("payments/", include("payments.urls")),
    # re_path(r'.*', TemplateView.as_view(template_name = 'index.html'), name="react-web"),
    #
    # RENEWAL URI - Need to Fix included - 새로 생성, 수정필요 포함
    #
    # path("address/", include("address.urls")),
    # path("auth/", include("auth.urls")),
    # path("exterminator/", include("exterminator.urls")),
    # path("farmer/", include("farmer.urls")),
    # path("payments/", include("payments.urls")),
    # path("user/", include("user.urls")),
]
