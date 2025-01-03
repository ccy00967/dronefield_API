from rest_framework import generics

from farmer.models import ArableLandInfo
from farmer.serializers import ArableLandInfoSerializer

from rest_framework import permissions
from farmer.permissions import OnlyOwnerCanUpdate



# 농지 정보 등록
class ArableLandInfoListView(generics.ListCreateAPIView):
    #queryset = ArableLandInfo.objects.all()
    #queryset = ArableLandInfo.objects.filter(request.user.)
    serializer_class = ArableLandInfoSerializer
    name = 'land_info_create_get_list'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        OnlyOwnerCanUpdate,
    )

    def get_queryset(self):
        return ArableLandInfo.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        #!중요 - 바로 시리얼라이저의 모델 owner에게 전달된다
        serializer.save(owner=self.request.user)


# 농지 정보 수정, 삭제
class ArableLandInfoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ArableLandInfo.objects.all()
    serializer_class = ArableLandInfoSerializer
    lookup_field = "uuid"
    name = 'uuid_land_update_delete'
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        OnlyOwnerCanUpdate,
    )
    

