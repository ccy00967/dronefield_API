from rest_framework import generics

from farmer.models import ArableLandInfo
from farmer.serializers import ArableLandInfoSerializer

from rest_framework import permissions
from farmer.permissions import OnlyOwnerCanUpdate
from rest_framework.response import Response
from rest_framework import status
from common.models import Address



# 농지목록 조회
class ArableLandInfoListView(generics.ListCreateAPIView):
    queryset = ArableLandInfo.objects.all()
    serializer_class = ArableLandInfoSerializer
    name = 'land_info_list'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    # 주소정보 모델 인스턴생 생성및 저장
    def perform_create(self, serializer):
        address = serializer.validated_data.pop('address')
        addressinfo = Address.objects.create(**address)
        arableland = ArableLandInfo.objects.create(
            address=addressinfo,
            **serializer.validated_data,
        )
        return arableland

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get('owner'):
            owner = self.request.query_params.get('owner')
            queryset = queryset.filter(owner__uuid=owner)
        return queryset

class ArableLandInfoCreateView(generics.CreateAPIView):
    queryset = ArableLandInfo.objects.all()
    serializer_class = ArableLandInfoSerializer
    name = 'land_info_create'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    # 주소정보 모델 인스턴생 생성및 저장
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# 농지 정보 조회, 수정, 삭제
class ArableLandInfoAPIView(generics.GenericAPIView):
    queryset = ArableLandInfo.objects.all()
    serializer_class = ArableLandInfoSerializer
    name = 'land_info_update_delete'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        OnlyOwnerCanUpdate,
    )

    def get_object(self, uuid):
        try:
            return ArableLandInfo.objects.get(uuid=uuid)
        except ArableLandInfo.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, uuid):
        land_info = self.get_object(uuid)
        serializer = ArableLandInfoSerializer(land_info)
        return Response(serializer.data)

    def patch(self, request, uuid):
        land_info = self.get_object(uuid)
        serializer = ArableLandInfoSerializer(land_info, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, uuid):
        land_info = self.get_object(uuid)
        land_info.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

