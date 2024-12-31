from drf_yasg import openapi


#회원가입
#UserRegistrationRequest = 
UserRegistrationResponse = {
            201: openapi.Response(
            description="201 CREATED",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'success': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="True"),
                    'message': openapi.Schema(type=openapi.TYPE_STRING, description="User successfully registered!"),
                }
            )),
            401: openapi.Response(
            description="401 UNAUTHORIZED",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING, description="email validation need first"),
                }
            )),
        }


#로그인
UserLoginResponse = {
            200: openapi.Response(
            description="200 OK",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'access': openapi.Schema(type=openapi.TYPE_STRING, description="Access Token"),
                    'refresh': openapi.Schema(type=openapi.TYPE_STRING, description="Refresh Token"),
                    'uuid': openapi.Schema(type=openapi.TYPE_STRING, description="user's UUID"),
                }
            )),
            400: openapi.Response(
            description="400 BAD_REQUEST",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING, description="Login Not Success"),
                }
            )),
        }