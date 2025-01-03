from rest_framework.permissions import BasePermission


class OnlyOwnerCanUpdate(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (obj.email == request.user.email and obj.uuid == request.user.uuid)
    
class OnlyManagerCanAccess(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.user.role == 2)

