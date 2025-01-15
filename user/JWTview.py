import json
import uuid
import redis

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import SignupSerializer

CustomUser = get_user_model()

# (예시) Redis 연결
# 실제 환경에 맞춰 host, port, password 등 설정 필요
r = redis.StrictRedis(host='localhost', port=6379, db=0)

class NiceCallbackView(APIView):
    """
    나이스에서 인증 완료 후, 콜백으로 결과가 들어오는 엔드포인트.
    - 나이스 측에서 전달하는 파라미터(예: 이름, 생년월일, 휴대폰번호, gender 등)를 수신
    - 이를 redis에 저장 (TTL: 30분 예시)
    - state(또는 nonce)라는 임시 키를 생성/또는 나이스 요청 시점에 이미 가지고 있을 수도 있음
    """

    def post(self, request):
        """
        나이스에서 콜백이 온다고 가정.
        ex) name, birthdate, mobileno, gender, nationalinfo 등이 들어온다고 가정
        실제로는 나이스 API에 맞춰 필드명 조정 필요
        """
        # 나이스에서 넘어오는 데이터 (예: request.data)
        name = request.data.get('name')
        birthdate = request.data.get('birthdate')
        mobileno = request.data.get('mobileno')
        gender = request.data.get('gender')  # "0" or "1"
        nationalinfo = request.data.get('nationalinfo')  # "0" or "1"
        state = request.data.get('state')  # 미리 FE에서 지정했거나, 여기가 인증 시작 시점일 수도

        if not all([name, birthdate, mobileno, gender, nationalinfo, state]):
            return Response({"detail": _("Invalid data from NICE callback.")}, status=status.HTTP_400_BAD_REQUEST)

        # Redis에 임시 저장
        # "nice_auth:{state}" 라는 키로, JSON 직렬화된 인증결과를 저장
        # TTL은 1800초(30분) 예시
        data_to_store = {
            "name": name,
            "birthdate": birthdate,
            "mobileno": mobileno,
            "gender": gender,
            "nationalinfo": nationalinfo,
        }
        r.setex(f"nice_auth:{state}", 1800, json.dumps(data_to_store))

        return Response({"detail": _("NICE callback success"), "state": state}, status=status.HTTP_200_OK)


class SignupView(APIView):
    """
    실제 회원가입을 진행하는 엔드포인트
    - 프론트엔드에서 state + email + password + 주소 정보 등을 함께 전송
    - Redis에서 본인인증 정보를 꺼내와서 최종 DB에 User를 생성
    - JWT 발급해서 반환
    """

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        state = serializer.validated_data['state']

        # Redis에서 본인인증 결과 가져오기
        redis_key = f"nice_auth:{state}"
        cached_data = r.get(redis_key)
        if not cached_data:
            return Response({"detail": _("No NICE auth data found or expired.")},
                            status=status.HTTP_400_BAD_REQUEST)

        # 인증 정보 파싱
        nice_data = json.loads(cached_data)
        name = nice_data['name']
        birthdate = nice_data['birthdate']
        mobileno = nice_data['mobileno']
        gender = nice_data['gender']
        nationalinfo = nice_data['nationalinfo']

        # 이제 serializer로부터 받은 회원가입 필드(이메일, 비번, 주소 등)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        road = serializer.validated_data['road']
        jibun = serializer.validated_data['jibun']
        detail = serializer.validated_data['detail']

        # UserManager를 이용해 최종 User 생성
        # 필요한 필드는 모두 keyword argument로 넘겨주면 됩니다.
        user = CustomUser.objects.create_user(
            email=email,
            password=password,
            name=name,
            birthdate=birthdate,
            mobileno=mobileno,
            gender=gender,
            nationalinfo=nationalinfo,
            road=road,
            jibun=jibun,
            detail=detail,
            is_active=True  # 가입 즉시 활성화한다면 True, 검증이 더 필요하다면 False
        )

        # 가입 성공: Redis에서 임시 데이터 삭제
        r.delete(redis_key)

        # JWT 발급 (SimpleJWT)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({
            "refresh": str(refresh),
            "access": access_token,
            "user_id": user.uuid,  # 혹은 user.id
            "email": user.email
        }, status=status.HTTP_201_CREATED)
