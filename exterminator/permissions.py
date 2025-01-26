from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    객체의 소유자만 접근을 허용하는 커스텀 권한 클래스
    """

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
"""
ADMIN = 1
MANAGER = 2
DRONE_EXTERMINATOR = 3
CUSTOMER = 4
"""


class OnlyOwnerExterminatorCanUpdate(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            obj.user.uuid == request.user.uuid and obj.user.email == request.user.email
        )


# # 신청서에 방제사 등록
# class OnlyExterminatorCanReadUpdate(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return request.user.role == 3


"""
EXTERMINATE_STATE = (
    (0, "matching"),
    (1, "preparing"),
    (2, "exterminating"),
    (3, "done"),
)
"""


class CheckExterminateState(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # 신청서에 방제사가 등록된 경우
        if obj.exterminateState == 1 and obj.exterminatorinfo != None:
            # 해당 방제사일 경우만 수정을 허가: for 방제수락 철회
            return obj.exterminatorinfo == request.user
        # 방제사 의뢰 수락
        return obj.exterminateState == 0
