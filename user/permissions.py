
# 이제보니까 request가 알아서 디코딩 되서 나온다!!!!
# 여기 파일은 무쓸모임 --------------------------
# 그래도 나중에 찾아볼 것을 대비해서 남겨두자

from rest_framework.permissions import BasePermission

# import jwt
# from config.settings.base import SIMPLE_JWT
# from rest_framework_simplejwt.authentication import JWTAuthentication

# 이때 토큰은 자동으로 decode된다
# request.user로 바로 사용가능
class OnlyOwnerCanUpdate(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (obj.email == request.user.email and obj.uuid == request.user.uuid)
    

class OnlyManagerCanAccess(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.user.role == 2)


        # 아래는 decode 방법 - 나중에 나이스 본인인증에 사용하기
        # try:
        #     decodedToken = jwt.decode(
        #         getRawAccessToken,
        #         SIMPLE_JWT['SIGNING_KEY'],
        #         algorithms=[SIMPLE_JWT['ALGORITHM']],
        #     )

        #     # 등록된 이메일이 같다면 수정을 허용 - 나중에 user_id로 수정할까?
        #     return obj.email == decodedToken.get('email')

        # except:
        #     return False


# 만약 그냥 일반 사용자 - GET, HEAD, OPTIONS 요청에만 True - 3개를 안전한 요청이라고 한다
# if request.method in permissions.SAFE_METHODS:
#     return True
# 만약 위의 3개중 하나가 아닌 경우 request.user가 obj.owner와 동일할때만 가능
# else:
#     return obj.email == request.email
# if obj.email == request.email:
#     return True
