from rest_framework import permissions


# class CheckUser(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if(request.user.role == 4):
#             return (request.user.uuid == obj.owner.uuid)
#         if(request.exterminatorinfo.role == 3):
#             return (request.user.uuid == obj.exterminatorinfo.uuid)
#         return False


# class CheckAmount(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         return (obj.requestAmount == request.data.get('requestAmount'))


# class CheckPaymentKey(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         # 만약 그냥 일반 사용자 - GET, HEAD, OPTIONS 요청에만 True - 3개를 안전한 요청이라고 한다
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return (obj.paymentKey == request.data.get('paymentKey'))


# # 방제 완료후에 결제 취소 방지
# class CheckStatusMatching(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         # 만약 그냥 일반 사용자 - GET, HEAD, OPTIONS 요청에만 True - 3개를 안전한 요청이라고 한다
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return (obj.exterminateState == 0)
