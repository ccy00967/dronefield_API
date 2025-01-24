from rest_framework import permissions

'''
ADMIN = 1
MANAGER = 2
DRONE_EXTERMINATOR = 3
CUSTOMER = 4
'''

class OnlyOwnerCanUpdate(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # 만약 그냥 일반 사용자 - GET, HEAD, OPTIONS 요청에만 True - 3개를 안전한 요청이라고 한다
        if request.method in permissions.SAFE_METHODS:
            return True
        # 만약 위의 3개중 하나가 아닌 경우 request.user가 obj.owner와 동일할때만 가능
        return (obj.owner.uuid == request.user.uuid and obj.owner.email == request.user.email)
    

class OnlyOnChargeExterminator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # obj.exterminator가 None인 경우를 처리
        if obj.exterminator is None:
            return False  # or True, 상황에 맞게 수정

        # obj.exterminator가 None이 아니면 uuid와 email을 비교
        return (obj.exterminator.uuid == request.user.uuid and obj.exterminator.email == request.user.email)
    

class isBeforePay(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # 만약 그냥 일반 사용자 - GET, HEAD, OPTIONS 요청에만 True - 3개를 안전한 요청이라고 한다
        if request.method in permissions.SAFE_METHODS:
            return True
        # 만약 위의 3개중 하나가 아닌 경우 request.user가 obj.owner와 동일할때만 가능
        return (obj.tosspayments == None)