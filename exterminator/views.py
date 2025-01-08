from rest_framework import generics
from rest_framework import permissions

from exterminator.permissions import OnlyOwnerExterminatorCanUpdate

from rest_framework.response import Response

from exterminator.models import Exterminator
from exterminator.models import ExterminatorLicense
from exterminator.serializers import ExterminatorSerializer
from exterminator.serializers import ExterminatorLicenseSerializer


# 방제사 정보
class ExterminatorView(generics.ListCreateAPIView):
    queryset = Exterminator.objects.all()
    serializer_class = ExterminatorSerializer
    lookup_field = "uuid"
    name = "exterminator-info"

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        OnlyOwnerExterminatorCanUpdate,
    ]


class ExterminatorLicenseView(generics.RetrieveUpdateAPIView):
    queryset = Exterminator.objects.all()
    serializer_class = ExterminatorLicenseSerializer
    lookup_field = "uuid"
    name = "exterminator-license"

    def patch(self, request, *args, **kwargs):
        # 'uuid'를 사용하여 Exterminator 객체를 찾음
        uuid = kwargs.get("uuid")
        # user__uuid=uuid는 Exterminator의 user 속성(즉, CustomUser 객체)의 uuid 필드가 요청받은 uuid와 일치하는 Exterminator 객체를 조회
        exterminator = Exterminator.objects.get(user__uuid=uuid)

        # Exterminator 객체에서 연결된 license 객체를 가져옴
        license_instance = exterminator.license

        # request의 데이터를 사용하여 license를 업데이트
        serializer = self.get_serializer(
            license_instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(request.data)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        OnlyOwnerExterminatorCanUpdate,
    ]
