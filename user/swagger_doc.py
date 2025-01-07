#from drf_yasg import openapi
'''
# 이메일
EmailRequest = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema('유저 이메일', type=openapi.TYPE_STRING, description="example@email.com"),
        },
    )

EmailResponse = {
        201: openapi.Response(
        description="201 CREATED",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING, description="email sended"),
            }
        )),
        500: openapi.Response(
        description="500 INTERNAL_SERVER_ERROR",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING, description="email send error"),
            }
        )),
    }

# 인증번호
ValidateRequest = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'validatekey': openapi.Schema('인증번호 필요(숫자 4자리)', type=openapi.TYPE_STRING),
        },
    )

ValidateResponse = {
        200: openapi.Response(
        description="200 OK",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING, description="email validated"),
            }
        )),
        401: openapi.Response(
        description="401 UNAUTHORIZED",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING, description="validate key error"),
            }
        )),
    }


#비밀번호
PasswordResetRequest = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'validatekey': openapi.Schema('인증번호 필요(숫자)', type=openapi.TYPE_STRING),
            'email': openapi.Schema('변경할 이메일 필요', type=openapi.TYPE_STRING),
            'password': openapi.Schema('new password', type=openapi.TYPE_STRING),
        },
    )

PasswordResetResponse = {
        200: openapi.Response(
        description="200 OK",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING, description="password updated"),
            }
        )),
        401: openapi.Response(
        description="401 UNAUTHORIZED",
        schema=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING, description="validate key error"),
            }
        )),
    }

#from drf_yasg import openapi


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
'''