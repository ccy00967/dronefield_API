from rest_framework import generics
from rest_framework import permissions
from rest_framework import status

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
    "Authorization": "Basic dGVzdF9za19Ma0tFeXBOQXJXV1lveEs5eldKQXJsbWVheFlHOg==",
    "Content-Type": "application/json",
}


# 신청서와 예약금 2개 만들기
# 이때 신청서를 여러개 받을 수 있다.
class RequestTossCreateAPIView(generics.CreateAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestTossUpdateSerializer
    name = "request-tosspayments-update"
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

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
                TotalAMOUNT += 10000

        # 값 검증하기
        url = "https://api.tosspayments.com/v1/payments/confirm"
        data = {"paymentKey": PAYMENT_KEY, "orderId": TOSSORDERID, "amount": TotalAMOUNT}
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
    lookup_field = "tossOrderId"
    name = "tosspayments-cancel"
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def post(self, request, *args, **kwargs):
        tossOrderId = self.kwargs.get('tossOrderId')  # URL에서 tossOrderId를 가져옴
        cancelReason = self.request.data.get("cancelReason")
        orderIdList = self.request.data.get("orderidlist")
        cancelAmount = 0

         # tossOrderId에 해당하는 TossPayments 객체를 찾기
        toss_payment = TossPayments.objects.filter(tossOrderId=tossOrderId).first()
        if toss_payment:
            PAYMENT_KEY = toss_payment.paymentKey  # TossPayments 객체에서 paymentKey를 가져옴
        else:
            return Response({"error": "TossPayments object not found."}, status=status.HTTP_404_NOT_FOUND)

        for orderid in orderIdList:
            try:
                # orderid를 'orderId'로 수정하여 필드명 일치시킴
                request_instance = Request.objects.get(orderId=orderid)
            except Request.DoesNotExist:
                return Response(
                    {"message": f"Request with orderId {orderid} does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # 사용자 타입에 따른 금액 계산
            if request.user.type == 3:
                cancelAmount += request_instance.reservateDepositAmount if request_instance.reservateDepositAmount else 1000
            elif request.user.type == 4:
                # 방제사가 예약한 신청서는 에러를 던지기
                if request_instance.exterminator is not None and request_instance.reservateDepositState != 0:
                    return Response(
                        {"message": "방제가 진행중인 신청서 입니다. 환불이 불가합니다."},
                        status=status.HTTP_406_NOT_ACCEPTABLE,
                    )
                cancelAmount += request_instance.requestAmount if request_instance.requestAmount else 0
                cancelAmount += 10000


        # 부분 환불하기
        url = "https://api.tosspayments.com/v1/payments/" + PAYMENT_KEY + "/cancel"
        data = {
            "cancelReason": cancelReason,
            "cancelAmount": cancelAmount,
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

        # 해당 신청서들 업데이트
        for orderid in orderIdList:
            if request.user.type == 3:
                Request.objects.filter(orderId=orderid).update(
                    exterminator=None,
                    exterminateState=0,
                    reservateTosspayments=None,
                    reservateDepositState=0,
                    depositCancelTransactionKey=tosspayData.transactionKey,
                )
            elif request.user.type == 4:
                Request.objects.filter(orderId=orderid).update(
                    requestDepositState=2,
                    requestCancelTransactionKey=tosspayData.transactionKey,
                )

        return Response(
            {"message": "결제가 취소되었습니다."}, status=status.HTTP_200_OK
        )
