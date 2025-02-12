from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
import uuid

from payments.serializers import RequestTossUpdateSerializer
from payments.serializers import TossPaymentsSerializer

# from payments.permissions import CheckUser
# from payments.permissions import CheckAmount
# from payments.permissions import CheckPaymentKey
# from payments.permissions import CheckStatusMatching

from trade.models import Request

import json
from payments.models import TossPayments
import requests
from rest_framework.response import Response


# 시크릿키를 base64로 인코딩 했다 - 토스 권장사항
# 터미널에 아래 명령어를 입력하면 인코딩된 값이 반환된다 - base64 임포트하거나 해서 사용하기
# echo -n 'test_sk_L~~~' | base64
HEADERS = {
    # 결제창 시크릿키(드론평야)
    "Authorization": "Basic dGVzdF9za19Ma0tFeXBOQXJXV1lveEs5eldKQXJsbWVheFlHOg==",
    # 결제 위젯 시크릿키(문서 공용)
    #"Authorization": "Basic dGVzdF9nc2tfZG9jc19PYVB6OEw1S2RtUVhrelJ6M3k0N0JNdzY=",
    "Content-Type": "application/json",
}


# 신청서와 예약금 2개 만들기
# 이때 신청서를 여러개 받을 수 있다.
class RequestTossCreateAPIView(generics.CreateAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestTossUpdateSerializer
    name = "request-tosspayments-update"
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def post(self, request):
        # 사용자로부터 받음
        PAYMENT_KEY = request.data.get("paymentKey")
        TOSSORDERID = request.data.get("tossOrderId")
        orderIdList = request.data.get("orderidlist")
        TotalAMOUNT = 0

        for orderid in orderIdList:
            try:
                # orderid를 'orderId'로 수정하여 필드명 일치시킴
                request_instance = Request.objects.get(orderId=orderid)
                
                if request.user.type == 3:
                    if request_instance.requestTosspayments != None:
                        return Response(
                            {"message": f"이미 결제가 완료된 신청서입니다."},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                elif request.user.type == 4:
                    if request_instance.reservateTosspayments != None:
                        return Response(
                            {"message": f"이미 결제가 완료된 신청서입니다."},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

            except Request.DoesNotExist:
                return Response(
                    {"message": f"Request with orderId {orderid} does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # RequestSerializer 인스턴스 생성
            serializer = self.get_serializer(request_instance)

            # 사용자 타입에 따른 금액 계산
            if request.user.type == 3:
                TotalAMOUNT += serializer.data.get("reservateDepositAmount", 1000)
            elif request.user.type == 4:
                TotalAMOUNT += serializer.data.get("requestAmount", 0)
                TotalAMOUNT += 10000  # 농민의 수수료 == 1만원

        # 값 검증하기
        url = "https://api.tosspayments.com/v1/payments/confirm"
        data = {
            "paymentKey": PAYMENT_KEY,
            "orderId": TOSSORDERID,
            "amount": TotalAMOUNT,
        }
        payload = json.dumps(data)
        response = requests.post(url, headers=HEADERS, data=payload)

        if 400 <= response.status_code < 500:
            error = response.json()
            return Response(
                {"code": error["code"], "message": error["message"]},
                status=response.status_code,
            )

        # 토스 결제확인 데이터
        tosspayData = response.json()

        # 토스 결제확인 데이터 저장
        tosspaymentsObj = TossPayments.objects.create(
            tossOrderId=tosspayData["orderId"],
            paymentKey=tosspayData["paymentKey"],
            method=tosspayData["method"],
            totalAmount=tosspayData["totalAmount"],
            status=tosspayData["status"],
        )

        # 해당 신청서들 업데이트
        for orderid in orderIdList:
            if request.user.type == 3:
                Request.objects.filter(orderId=orderid).update(
                    exterminator=request.user,
                    exterminateState=1,
                    reservateTosspayments=tosspaymentsObj,
                    reservateDepositState=1,
                )
            elif request.user.type == 4:
                Request.objects.filter(orderId=orderid).update(
                    requestTosspayments=tosspaymentsObj,
                    requestDepositState=1,
                )

        return Response(
            {"message": "결제가 완료되었습니다."}, status=status.HTTP_201_CREATED
        )


# 결제 취소 - 방제사가 예약한 신청서는 결제 취소 불가능
class TossPaymentsUpdateDeleteView(generics.RetrieveUpdateAPIView):
    queryset = TossPayments.objects.all()
    serializer_class = TossPaymentsSerializer
    name = "tosspayments-cancel"
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        # TODO: 본인이 결제한 것만 결제 취소 가능하게 퍼미션 추가하기
    )

    def post(self, request, *args, **kwargs):
        cancelReason = self.request.data.get("cancelReason")
        orderid = self.request.data.get("orderid")  # 신청서 UUID
        paymentKey = ""
        amout = 0
        tossOrderId = ""

        try:
            request_instance = Request.objects.get(orderId=orderid)
        except Exception as e:
            return Response(
                {"message": f"신청서 정보를 찾을 수 없습니다! : 유효하지 않은 orderid"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # 농민
        if request.user.type == 4:
            if request_instance.requestCancelTransactionKey != "":
                return Response(
                    {"message": f"이미 결제가 취소된 신청서입니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            tossOrderId = request_instance.requestTosspayments.tossOrderId
            paymentKey = request_instance.requestTosspayments.paymentKey
            amout = request_instance.requestAmount
            amout += 10000  # 농민의 수수료 == 10000원

            # 방제가 진행중인, 방제사가 예약한 신청서는 에러를 던지기
            if (
                request_instance.exterminator is not None
                and request_instance.reservateDepositState != 0
            ):
                return Response(
                    {"message": "방제가 진행중인 신청서 입니다. 환불이 불가합니다."},
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
        # 방제사
        elif request.user.type == 3:
            if request_instance.depositCancelTransactionKey != "":
                return Response(
                    {"message": f"이미 결제가 취소된 신청서입니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            tossOrderId = request_instance.reservateTosspayments.tossOrderId
            paymentKey = request_instance.reservateTosspayments.paymentKey
            amout = request_instance.reservateDepositAmount  # 방제사의 수수료 == 1000원

        # # tossOrderId에 해당하는 TossPayments 객체를 찾기
        toss_payment = TossPayments.objects.filter(tossOrderId=tossOrderId).first()

        if not toss_payment:
            return Response(
                {"error": "신청서에 연결된 결제 정보를 찾을 수 없습니다!, 결제가 정상적으로 이루어진 신청서가 아닙니다."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # 부분 환불하기
        url = "https://api.tosspayments.com/v1/payments/" + paymentKey + "/cancel"
        data = {
            "cancelReason": cancelReason,
            "cancelAmount": amout,
        }
        payload = json.dumps(data)
        headers = HEADERS
        response = requests.post(url, headers=headers, data=payload)

        if 400 <= response.status_code < 500:
            error = response.json()
            return Response(
                {"code": error["code"], "message": error["message"]},
                status=response.status_code,
            )

        # 토스 결제확인 데이터
        tosspayData = response.json()

        # toss_payment 인스턴스를 직접 수정하고 저장하기
        toss_payment.status = tosspayData["status"]
        toss_payment.save()

        # 해당 신청서 업데이트
        if request.user.type == 3:
            Request.objects.filter(orderId=orderid).update(
                exterminator=None,
                exterminateState=0,
                reservateTosspayments=None,
                reservateDepositState=0,
                depositCancelTransactionKey=tosspayData.get("cancels")[0].get(
                    "transactionKey"
                ),
            )
        elif request.user.type == 4:
            Request.objects.filter(orderId=orderid).update(
                requestDepositState=2,
                requestCancelTransactionKey=tosspayData.get("cancels")[0].get(
                    "transactionKey"
                ),
            )

        return Response(
            {"message": "결제가 취소되었습니다."}, status=status.HTTP_200_OK
        )


# 테스트용 결제 없이 방제사 정보 등록하기
class RequestTossExterminatorCreateAPIView(generics.CreateAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestTossUpdateSerializer
    name = "request-test-for-exterminator"
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def post(self, request):
        # 사용자로부터 받음
        PAYMENT_KEY = request.data.get("paymentKey")
        TOSSORDERID = request.data.get("tossOrderId")
        orderIdList = request.data.get("orderidlist")
        TotalAMOUNT = 0

        for orderid in orderIdList:
            try:
                # orderid를 'orderId'로 수정하여 필드명 일치시킴
                request_instance = Request.objects.get(orderId=orderid)
                
                if request.user.type == 3:
                    if request_instance.requestTosspayments != None:
                        return Response(
                            {"message": f"이미 결제가 완료된 신청서입니다."},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                elif request.user.type == 4:
                    if request_instance.reservateTosspayments != None:
                        return Response(
                            {"message": f"이미 결제가 완료된 신청서입니다."},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

            except Request.DoesNotExist:
                return Response(
                    {"message": f"Request with orderId {orderid} does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # RequestSerializer 인스턴스 생성
            serializer = self.get_serializer(request_instance)

            # 사용자 타입에 따른 금액 계산
            if request.user.type == 3:
                TotalAMOUNT += serializer.data.get("reservateDepositAmount", 1000)
            elif request.user.type == 4:
                TotalAMOUNT += serializer.data.get("requestAmount", 0)
                TotalAMOUNT += 10000  # 농민의 수수료 == 1만원

        '''
        # 값 검증하기
        url = "https://api.tosspayments.com/v1/payments/confirm"
        data = {
            "paymentKey": PAYMENT_KEY,
            "orderId": TOSSORDERID,
            "amount": TotalAMOUNT,
        }
        payload = json.dumps(data)
        response = requests.post(url, headers=HEADERS, data=payload)

        if 400 <= response.status_code < 500:
            error = response.json()
            return Response(
                {"code": error["code"], "message": error["message"]},
                status=response.status_code,
            )

        # 토스 결제확인 데이터
        tosspayData = response.json()

        '''

        # 토스 결제확인 데이터 저장
        tosspaymentsObj = TossPayments.objects.create(
            tossOrderId=uuid.uuid4(),
            paymentKey=uuid.uuid4(),
            method="CARD",
            totalAmount=1000,
            status="test_status",
        )

        # 해당 신청서들 업데이트
        for orderid in orderIdList:
            if request.user.type == 3:
                Request.objects.filter(orderId=orderid).update(
                    exterminator=request.user,
                    exterminateState=1,
                    reservateTosspayments=tosspaymentsObj,
                    reservateDepositState=1,
                )
            elif request.user.type == 4:
                Request.objects.filter(orderId=orderid).update(
                    requestTosspayments=tosspaymentsObj,
                    requestDepositState=1,
                )

        return Response(
            {"message": "결제가 완료되었습니다."}, status=status.HTTP_201_CREATED
        )


# 테스트용 결제 취소 - 실제 토스에 요청없이 결제취소를 흉내낸다,
class TossPaymentsExterminatorDeleteView(generics.RetrieveUpdateAPIView):
    queryset = TossPayments.objects.all()
    serializer_class = TossPaymentsSerializer
    name = "tosspayments-test-cancel"
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        # TODO: 본인이 결제한 것만 결제 취소 가능하게 퍼미션 추가하기
    )

    def post(self, request, *args, **kwargs):
        cancelReason = self.request.data.get("cancelReason")
        orderid = self.request.data.get("orderid")  # 신청서 UUID
        paymentKey = ""
        amout = 0
        tossOrderId = ""

        try:
            request_instance = Request.objects.get(orderId=orderid)
        except Exception as e:
            return Response(
                {"message": f"신청서 정보를 찾을 수 없습니다! : 유효하지 않은 orderid"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # 농민
        if request.user.type == 4:
            if request_instance.requestCancelTransactionKey != "":
                return Response(
                    {"message": f"이미 결제가 취소된 신청서입니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            tossOrderId = request_instance.requestTosspayments.tossOrderId
            paymentKey = request_instance.requestTosspayments.paymentKey
            amout = request_instance.requestAmount
            amout += 10000  # 농민의 수수료 == 10000원

            # 방제가 진행중인, 방제사가 예약한 신청서는 에러를 던지기
            if (
                request_instance.exterminator is not None
                and request_instance.reservateDepositState != 0
            ):
                return Response(
                    {"message": "방제가 진행중인 신청서 입니다. 환불이 불가합니다."},
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                )
        # 방제사
        elif request.user.type == 3:
            if request_instance.depositCancelTransactionKey != "":
                return Response(
                    {"message": f"이미 결제가 취소된 신청서입니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            tossOrderId = request_instance.reservateTosspayments.tossOrderId
            paymentKey = request_instance.reservateTosspayments.paymentKey
            amout = request_instance.reservateDepositAmount  # 방제사의 수수료 == 1000원

        '''
        # # tossOrderId에 해당하는 TossPayments 객체를 찾기
        toss_payment = TossPayments.objects.filter(tossOrderId=tossOrderId).first()

        if not toss_payment:
            return Response(
                {"error": "신청서에 연결된 결제 정보를 찾을 수 없습니다!, 결제가 정상적으로 이루어진 신청서가 아닙니다."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # 부분 환불하기
        url = "https://api.tosspayments.com/v1/payments/" + paymentKey + "/cancel"
        data = {
            "cancelReason": cancelReason,
            "cancelAmount": amout,
        }
        payload = json.dumps(data)
        headers = HEADERS
        response = requests.post(url, headers=headers, data=payload)

        if 400 <= response.status_code < 500:
            error = response.json()
            return Response(
                {"code": error["code"], "message": error["message"]},
                status=response.status_code,
            )

        # 토스 결제확인 데이터
        tosspayData = response.json()

        # toss_payment 인스턴스를 직접 수정하고 저장하기
        toss_payment.status = tosspayData["status"]
        toss_payment.save()

        toss_payment.status = "CANCEL"
        toss_payment.save()
        '''

        # 해당 신청서 업데이트
        if request.user.type == 3:
            Request.objects.filter(orderId=orderid).update(
                exterminator=None,
                exterminateState=0,
                reservateTosspayments=None,
                reservateDepositState=0,
                depositCancelTransactionKey=uuid.uuid4(),
            )
        elif request.user.type == 4:
            Request.objects.filter(orderId=orderid).update(
                requestDepositState=2,
                requestCancelTransactionKey=uuid.uuid4(),
            )

        return Response(
            {"message": "결제가 취소되었습니다."}, status=status.HTTP_200_OK
        )
