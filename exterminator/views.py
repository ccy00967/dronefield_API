from rest_framework import generics
from rest_framework import permissions

from exterminator.permissions import OnlyOwnerExterminatorCanUpdate

from rest_framework.response import Response

from exterminator.models import Exterminator
from exterminator.models import ExterminatorLicense
from exterminator.serializers import ExterminatorSerializer
from exterminator.serializers import ExterminatorLicenseSerializer


# TODO: 현재 해당 로직은 사용자로부터 라이센스를 받아서 업데이트 할 수 없음. 둘 중 하나로 수정 필요
# 1. 라이센스 정보를 팩스 등, 수동으로 받아서 DB에 우리가 업로드
# 2. 라이센스 정보를 사용자로부터 받아서 업데이트
# a. 어쨌든 두 방법 모두 농민이, 본인 담당 방제사 정보를 불러올때 Exterminator 객체를 불러오게 대규모 수정해야함


# 방제사 정보
class ExterminatorView(generics.ListCreateAPIView):
    serializer_class = ExterminatorSerializer
    name = "exterminator-info"
    lookup_field = "uuid"
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        OnlyOwnerExterminatorCanUpdate,
    ]

    def get_queryset(self):
        # URL에서 uuid 추출 후, 해당 uuid에 해당하는 Exterminator들을 한 번에 조회
        return Exterminator.objects.filter(user__uuid=self.kwargs['uuid'])


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
